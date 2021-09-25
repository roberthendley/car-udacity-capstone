from datetime import date, datetime
from flask import Blueprint, request, abort, jsonify
from sqlalchemy.sql.sqltypes import DateTime
from .models import Report, ReportItem, DEFAULT_PAGE_SIZE
from sqlalchemy.exc import DatabaseError
from ..auth.auth import requires_auth

blueprint = Blueprint('reports', __name__)

def is_valid_report(header: dict, items: list) -> bool:

    # TODO: Complete report validation
    pass


def read_detailed_report(report: Report):
    report_items = ReportItem.query.join(
        Report).filter(ReportItem.report_id == report.id)
    requested_tasks = report_items.filter(
        ReportItem.item_type == 'requested_task').all()
    work_undertaken = report_items.filter(
        ReportItem.item_type == 'work_undertaken').all()
    follow_up_tasks = report_items.filter(
        ReportItem.item_type == 'follow_up_task').all()
    customer_tasks = report_items.filter(
        ReportItem.item_type == 'customer_task').all()
    issues_identified = report_items.filter(
        ReportItem.item_type == 'issue_identified').all()

    report_data = dict()
    report_data['id'] = report.id
    report_data['header'] = report.format()

    report_items = dict()
    report_items['requested_tasks'] = [item.format()
                                       for item in requested_tasks]
    report_items['work_undertaken'] = [item.format()
                                       for item in work_undertaken]
    report_items['follow_up_tasks'] = [item.format()
                                       for item in follow_up_tasks]
    report_items['customer_tasks'] = [item.format() for item in customer_tasks]
    report_items['issues_identified'] = [item.format()
                                         for item in issues_identified]
    report_data['report_items'] = report_items

    return report_data


def set_report_item_dtls(report_item: dict, item_type: str):
    report_item['item_type'] = item_type
    return report_item


def read_report_items(report_data: dict):
    requested_tasks = report_data.get('requested_tasks', list)
    work_undertaken = report_data.get('work_undertaken', list)
    follow_up_tasks = report_data.get('follow_up_tasks', list)
    customer_tasks = report_data.get('customer_tasks', list)
    issues_identified = report_data.get('issues_identified', list)

    requested_tasks = [set_report_item_dtls(
        item, 'requested_task') for item in requested_tasks]
    work_undertaken = [set_report_item_dtls(
        item, 'work_undertaken') for item in work_undertaken]
    follow_up_tasks = [set_report_item_dtls(
        item, 'follow_up_task') for item in follow_up_tasks]
    customer_tasks = [set_report_item_dtls(
        item, 'customer_task') for item in customer_tasks]
    issues_identified = [set_report_item_dtls(
        item, 'issue_identified') for item in issues_identified]

    return requested_tasks + work_undertaken + follow_up_tasks + customer_tasks + issues_identified


def read_report_header(report_data: dict):
    report_header = dict()
    report_header['client_id'] = report_data.get('client_id', int),
    report_header['client_contact_id'] = report_data.get(
        'client_contact_id', int),
    report_header['consulant_id'] = report_data.get('consulant_id', int)
    report_header['client_manager_id'] = report_data.get(
        'client_manager_id', int)
    report_header['report_date'] = report_data.get('report_date', date)
    report_header['report_from_date'] = report_data.get(
        'report_from_date', date)
    report_header['report_to_date'] = report_data.get('report_to_date', date)
    report_header['engagement_reference'] = report_data.get(
        'engagement_reference')
    report_header['report_status'] = report_data.get('report_status')

    return report_header


def delete_report_items(report_id):
    report_items = ReportItem.query.filter(
        ReportItem.report_id == report_id).all()

    if len(report_items) > 0:
        for item in report_items:
            item.delete()


# ---------------------------------------------------
# Route - Get reports list
# ----------------------------------------------------
@blueprint.route('/api/reports', methods=['GET'])
@requires_auth('read:Reports')
def get_reports():

    reports = Report.query

    # Apply Client Id Filter
    if request.args.get('client_id'):
        reports = reports.filter(Report.client_id == request.args.get('client_id', type=int))
    
    # Apply Consultant Id Filter
    if request.args.get('consultant_id'):
        reports = reports.filter(Report.consulant_id == request.args.get('consultant_id', type=int))
    
    # Apply From Date Range
    if request.args.get('from_date'):
        from_date = datetime.fromisoformat(request.args.get('from_date'))
        reports = reports.filter(Report.report_date >= from_date)
    
    # Apply From Date Range
    if request.args.get('to_date'):
        to_date = datetime.fromisoformat(request.args.get('to_date'))
        reports = reports.filter(Report.report_date <= to_date)

    # Set the paging details
    page_size = request.args.get('page_size', default=DEFAULT_PAGE_SIZE, type=int)
    page = request.args.get('page', default=1, type=int)
    reports_page = reports.order_by(Report.report_date.desc()).paginate(page, page_size, False)
    reports = reports_page.items

    if len(reports) == 0:
        abort(404)

    report_list = [report.format() for report in reports]
    return jsonify({
        'success': True,
        'page': reports_page.page,
        'pages': reports_page.pages,
        'data': report_list
    })


# ---------------------------------------------------
# Route - Get a Report
# ----------------------------------------------------
@blueprint.route('/api/reports/<int:id>', methods=['GET'])
@requires_auth('read:reports')
def get_report(id: int):
    report: Report = Report.query.get_or_404(id)
    report_data = read_detailed_report(report)

    return jsonify({
        'success': True,
        'data': report_data
    })


# ---------------------------------------------------
# Route - Create new Report
# ----------------------------------------------------
@blueprint.route('/api/reports', methods=['POST'])
@requires_auth('create:reports')
def add_report():
    body_data: dict = request.get_json()

    if not body_data:
        abort(400)

    report_header = read_report_header(body_data['header'])
    report_items = read_report_items(body_data['report_items'])

    # TODO validate the report item data

    try:
        # Create the Report
        report = Report()
        report.from_dict(report_header)
        report.insert()

        report_item_id = 0
        for item in report_items:
            report_item_id += 1
            item['report_id'] = report.id
            item['report_item_nbr'] = report_item_id

            report_item = ReportItem()
            report_item.from_dict(item)
            report_item.insert()

        # After all the repoirt items have been saved, read back the full report
        report_data = read_detailed_report(report)

        return jsonify({
            "success": True,
            "message": "The report has been successfully saved",
            # "data": {}
            "data": report_data
        }), 200

    except DatabaseError as db_error:
        print(db_error)
        abort(400)

    except Exception as error:
        print(error)
        abort(500)


# ---------------------------------------------------
# Route - Update a Report
# ----------------------------------------------------
@blueprint.route('/api/reports/<int:id>', methods=['PATCH'])
@requires_auth('update:reports')
def update_report(id: int):
    report: Report = Report.query.get_or_404(id)
    body_data: dict = request.get_json()

    if not body_data:
        abort(400)

    report_header = read_report_header(body_data['header'])
    report_items = read_report_items(body_data['report_items'])

    try:
        report.from_dict(report_header)
        report.update()

        delete_report_items(id)
        report_item_id = 0
        for item in report_items:
            report_item_id += 1
            item['report_id'] = report.id
            item['report_item_nbr'] = report_item_id

            report_item = ReportItem()
            report_item.from_dict(item)
            report_item.insert()

        return jsonify({
            "success": True,
            "message": "The report has been successfully saved",
            "data": report.format()
        }), 200

    except DatabaseError as db_error:
        print(db_error)
        abort(400)

    except Exception as error:
        print(error)
        abort(500)

# ---------------------------------------------------
# Route - Update a Report
# ----------------------------------------------------
@blueprint.route('/api/reports/<int:id>', methods=['DELETE'])
@requires_auth('delete:reports')
def delete_report(id: int):
    report: Report = Report.query.get_or_404(id)

    try:
        report.delete()

        return jsonify({
            "success": True,
            "message": "The report has been successfully delete",
        }), 200

    except DatabaseError as db_error:
        print(db_error)
        abort(400)

    except Exception as error:
        print(error)
        abort(500)
from datetime import date, datetime
from flask import Blueprint, request, abort, jsonify
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy import func
from ..models import Report, ReportItem, DEFAULT_PAGE_SIZE
from sqlalchemy.exc import DatabaseError
from auth.auth import requires_auth

blueprint = Blueprint('reports', __name__)


def is_valid_report(header: dict, items: list) -> bool:

    # TODO: Complete report validation
    pass



# ---------------------------------------------------
# Route - Get reports list
# ----------------------------------------------------
@blueprint.route('/api/reports', methods=['GET'])
@requires_auth('read:reports')
def get_reports():

    reports = Report.query

    # Apply Client Id Filter
    if request.args.get('client_id'):
        reports = reports.filter(
            Report.client_id == request.args.get('client_id', type=int))

    # Apply Consultant Id Filter
    if request.args.get('consultant_id'):
        reports = reports.filter(
            Report.consulant_id == request.args.get('consultant_id', type=int))

    # Apply From Date Range
    if request.args.get('from_date'):
        from_date = datetime.fromisoformat(request.args.get('from_date'))
        reports = reports.filter(Report.report_date >= from_date)

    # Apply From Date Range
    if request.args.get('to_date'):
        to_date = datetime.fromisoformat(request.args.get('to_date'))
        reports = reports.filter(Report.report_date <= to_date)

    # Set the paging details
    page_size = request.args.get(
        'page_size', default=DEFAULT_PAGE_SIZE, type=int)
    page = request.args.get('page', default=1, type=int)
    reports_page = reports.order_by(
        Report.report_date.desc()).paginate(page, page_size, False)
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
    detailed = request.args.get('detailed', default=0, type=int)

    if detailed == 0:
        report_data = report.format()
    elif detailed == 1:
        report_data = report.format_detailed()
    else:
        abort(400)

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

    
    # TODO validate the report item data

    try:
        # Create the Report
        report = Report()
        report.from_dict(body_data)
        report.report_status = "new"
        report.insert()

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
@blueprint.route('/api/reports/<int:id>', methods=['PATCH'])
@requires_auth('update:reports')
def update_report(id: int):
    report: Report = Report.query.get_or_404(id)
    body_data: dict = request.get_json()

    if not body_data:
        abort(400)

    try:
        report.from_dict(body_data)
        report.update()

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
# Route - Delete a Report
# ----------------------------------------------------
@blueprint.route('/api/reports/<int:id>', methods=['DELETE'])
@requires_auth('delete:reports')
def delete_report(id: int):
    report: Report = Report.query.get_or_404(id)

    try:
        report.delete()

        return jsonify({
            "success": True,
            "message": "The report has been successfully deleted",
        }), 200

    except DatabaseError as db_error:
        print(db_error)
        abort(400)

    except Exception as error:
        print(error)
        abort(500)


# ---------------------------------------------------
# Route - Update a Report Item
# ----------------------------------------------------
@blueprint.route('/api/reports/<int:report_id>/items/<int:item_id>', methods=['PATCH'])
@requires_auth('update:report-items')
def update_report_item(report_id: int, item_id: int):
    report_item: ReportItem = ReportItem.query.filter(
        ReportItem.report_id == report_id,
        ReportItem.report_item_nbr == item_id).first()

    if not report_item:
        abort(404)

    body_data: dict = request.get_json()

    if not body_data:
        abort(400)

    try:
        report_item.from_dict(body_data)
        report_item.update()

        return jsonify({
            "success": True,
            "message": "The report item has been successfully updated",
            "data": report_item.format()
        }), 200

    except DatabaseError as db_error:
        print(db_error)
        abort(400)

    except Exception as error:
        print(error)
        abort(500)


# ---------------------------------------------------
# Route - Get the specified report report-items
# ----------------------------------------------------
@blueprint.route('/api/reports/<int:report_id>/items', methods=['GET'])
@requires_auth('read:report-items')
def get_report_items(report_id: int):

    report_items = ReportItem.query.filter(
        ReportItem.report_id == report_id).all()

    if len(report_items) == 0:
        abort(404)

    report_item_list = [report_item.format() for report_item in report_items]
    return jsonify({
        'success': True,
        'data': report_item_list
    })

# ---------------------------------------------------
# Route - Get the specified report item
# ----------------------------------------------------
@blueprint.route('/api/reports/<int:report_id>/items/<int:item_id>', methods=['GET'])
@requires_auth('read:report-items')
def get_report_item(report_id: int, item_id:int):

    report_item: ReportItem = ReportItem.query.filter(
        ReportItem.report_id == report_id,
        ReportItem.report_item_nbr == item_id).first()

    if not report_item:
        abort(404)

    return jsonify({
        'success': True,
        'data': report_item.format()
    })

# ---------------------------------------------------
# Route - Add a Report Item
# ----------------------------------------------------
@blueprint.route('/api/reports/<int:report_id>/items', methods=['POST'])
@requires_auth('create:report-items')
def add_report_item(report_id: int):

    body_data: dict = request.get_json()

    if not body_data:
        abort(400)

    max_report_item = ReportItem.query(func.max(ReportItem.report_item_nbr)).filter(
        ReportItem.report_id == report_id).scalar()

    if not max_report_item:
        max_report_item = 0

    try:
        report_item = ReportItem()
        report_item.report_id = report_id
        report_item.report_item_nbr = max_report_item + 1
        report_item.from_dict(body_data)
        report_item.insert()

        return jsonify({
            "success": True,
            "message": "The report item has been successfully deleted",
        }), 200

    except DatabaseError as db_error:
        print(db_error)
        abort(400)

    except Exception as error:
        print(error)
        abort(500)


# ---------------------------------------------------
# Route - Update a Report Item
# ----------------------------------------------------
@blueprint.route('/api/reports/<int:report_id>/items/<int:item_id>', methods=['PATCH'])
@requires_auth('update:report-items')
def update_report_item(report_id: int, item_id: int):
    report_item: ReportItem = ReportItem.query.filter(
        ReportItem.report_id == report_id,
        ReportItem.report_item_nbr == item_id).first()

    if not report_item:
        abort(404)

    body_data: dict = request.get_json()

    if not body_data:
        abort(400)

    try:
        report_item.from_dict(body_data)
        report_item.update()

        return jsonify({
            "success": True,
            "message": "The report item has been successfully updated",
            "data": report_item.format()
        }), 200

    except DatabaseError as db_error:
        print(db_error)
        abort(400)

    except Exception as error:
        print(error)
        abort(500)

# ---------------------------------------------------
# Route - Delete a Report Item
# ----------------------------------------------------
@blueprint.route('/api/reports/<int:report_id>/items/<int:item_id>', methods=['DELETE'])
@requires_auth('delete:report-items')
def delete_report_item(report_id: int, item_id: int):
    report_item: ReportItem = ReportItem.query.filter(
        ReportItem.report_id == report_id,
        ReportItem.report_item_nbr == item_id).first()

    if not report_item:
        abort(404)

    try:
        report_item.delete()

        return jsonify({
            "success": True,
            "message": "The report item has been successfully deleted",
        }), 200

    except DatabaseError as db_error:
        print(db_error)
        abort(400)

    except Exception as error:
        print(error)
        abort(500)

# Reports

## Get a list of Reports
Get a list of reports saved for client work 

* **URL**

  `/api/reports`

* **Method:**
  
  `GET`
  
*  **URL Params**

   **Required:**
 
   None

   **Optional:**
 
    <table>
        <thead>
            <tr>
                <th>Parameter</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>`client=[alphanumeric]`</td>
                <td>Limit the reports returned in the list to client names that match the search criteria</td>
            </tr>
            <tr>
                <td>`consultant=[alphanumeric]`</td>
                <td>Limit the reports returned in the list to consultants names that match the search criteria</td>
            </tr>
            <tr>
                <td>`from_date=[Date]`</td>
                <td>Limit the reports returned in the list to reports greater than or equal to the nominated date. Dates should be in the format YYYY-MM-DD</td>
            </tr>
            <tr>
                 <td>`to_date=[Date]`</td>
                <td>Limit the reports returned in the list to reports less than or equal to the nominated date. Dates should be in the format YYYY-MM-DD</td>
            </tr>
            <tr>
                <td>`page_size=[integer]`</td>
                <td>Limit the number of records return by the query. The default page size is 20 record</td>
            </tr>
            <tr>
                <td>`page=[integer]`</td>
                <td>Select the page number to return</td>
            </tr>
        </tbody>
    </table>



* **Data Params**

  None

* **Headers**

    <table>
        <thead>
            <tr>
                <th>Header</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>`Authorization`</td>
                <td>JWT Bearer token e.g. `Bearer 566767y7866nbjshahu78y678...`</td>
            </tr>
        </tbody>
    </table>

* **Success Response:**
  
    * **Code:** 200 <br />
    **Content:** 
    ```json
    { 
        "success" : true,
        "page": 1,
        "pages": 5,
        "data": [{
            "id": 1,
            "client_id": 2,
            "client_name": "ABC Company",
            "client_contact_id": 1,
            "contact_name": "Sarah Young",
            "consultant_id": 2,
            "consultant_name": "David Ford",
            "client_manager_id": 3,
            "client_manager_name": "",
            "report_date": "2021-08-05",
            "report_from_date": "2021-07-30",
            "report_to_date": "2021-07-31",
            "engagement_reference": "LC1234",
            "report_status": "new"
        }] 
    }
    ```
 
* **Sample Call:**

    ```console
    $ curl --request GET 'http://127.0.0.1:5000/api/reports?client_id=1' \
     --header 'Authorization: Bearer VCIsImtpZCI6...'
    ```
  

* **Notes:**

  <_This is where all uncertainties, commentary, discussion etc. can go. I recommend timestamping and identifying oneself when leaving comments here._>


## Get a nominated report
Get a list of reports saved for client work 

* **URL**

  `/api/reports/:id`

* **Method:**
  
  `GET`
  
*  **URL Params**

   **Required:**
 
   <table>
        <thead>
            <tr>
                <th>Parameter</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>`id=[integer]`</td>
                <td>Id number of the report</td>
            </tr>
        </tbody>
    </table>

   **Optional:**
 
    None

* **Data Params**

  None

* **Headers**

    <table>
        <thead>
            <tr>
                <th>Header</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>`Authorization`</td>
                <td>JWT Bearer token e.g. `Bearer 566767y7866nbjshahu78y678...`</td>
            </tr>
        </tbody>
    </table>

* **Success Response:**
  
    * **Code:** 200 <br />
    **Content:** 
    ```json
    { 
        success : true,
        data: {
            id: 1,
            client_id: 2,
            client_name: 'ABC Company',
            client_contact_id: 1,
            contact_name: 'Sarah Young',
            consultant_id: 2,
            consultant_name: 'David Ford',
            client_mgr_id: 3,
            client_mgr_name: 'Emma Mears',
            report_date: '2021-08-05',
            engagement_reference: 'LC1234',
            report_from_date: '2021-08-01',
            report_to_date: '2021-08-05',
            requested_tasks: [],
            
        } 
    }
    ```
 
* **Error Responses:**

  * **Code:** 400 Bad Request <br />
    **Content:** `{ error : "Log in" }`

    OR

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "Log in" }`

    OR

  * **Code:** 405 UNPROCESSABLE ENTRY <br />
    **Content:** `{ error : "Email Invalid" }`

    OR

  * **Code:** 500 Server Error <br />
    **Content:** `{ error : "Email Invalid" }`

* **Sample Call:**

    ```console
    curl ..........

    ```
  

* **Notes:**

  <_This is where all uncertainties, commentary, discussion etc. can go. I recommend timestamping and identifying oneself when leaving comments here._>
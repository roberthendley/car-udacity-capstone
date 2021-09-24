# Clients

Clients
## Get a list of Clients
Get a list of clients in the application

* **URL**

  `/api/clients`

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
                <td>`search=[alphanumeric]`</td>
                <td>Limit the reports returned in the list to client names that match the search criteria</td>
            </tr>
            <tr>
                <td>`page_size=[integer]`</td>
                <td>Limit the number of records return by the query. The default page size is 20 record</td>
            </tr>
            <tr>
                <td>`page=[integer]`</td>
                <td>Select the page number to return. The default page is one</td>
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
        "pages": 5
        "data": [{
            "id": 1,
            "name": "ABC Company",
            "bus_reg_nbr": "01234567890",
            "abbreviation": "ABCC"
        }] 
    }
    ```
 
* **Sample Call:**

    ```console
    $ curl --location --request GET 'http://127.0.0.1:5000/api/clients?page=1' \
    --header 'Authorization: Bearer VCIsImtpZCI6...'
    ```

## Add a client
Add a new client

* **URL**

  `/api/clients`

* **Method:**
  
  `POST`
  
*  **URL Params**

   **Required:**
 
   None

   **Optional:**
 
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
            <tr>
                <td>`Content-Type`</td>
                <td>`application/json`</td>
            </tr>
        </tbody>
    </table>

* **Request Body**

    ```json
    {
        "name": "string",
        "bus_reg_nbr": "string",
        "abbreviation": "string"
    }
    ```


* **Success Response:**
  
    * **Code:** 200 <br />
    **Content:** 
    ```json
    { 
        "success" : true,
        "data": {
            "abbreviation": "RSC",
            "bus_reg_nbr": "10123456789",
            "id": 1,
            "name": "Regional Shire Council"
        }
    }
    ```
   

## Get a nominated client
Get a specific client

* **URL**

  `/api/clients/:id`

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
                <td>Id number of the client</td>
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
        "success" : true,
        "data": {
            "abbreviation": "RSC",
            "bus_reg_nbr": "10123456789",
            "id": 1,
            "name": "Regional Shire Council"
        }
    }
    ```
 
## Update a nominated client
Get a specific client

* **URL**

  `/api/clients/:id`

* **Method:**
  
  `PATCH`
  
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
                <td>Id number of the client</td>
            </tr>
        </tbody>
    </table>

   **Optional:**
 
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
            <tr>
                <td>`Content-Type`</td>
                <td>`application/json`</td>
            </tr>
        </tbody>
    </table>

* **Request Body**

    ```json
    {
        "name": "string",
        "bus_reg_nbr": "string",
        "abbreviation": "string"
    }
    ```


* **Success Response:**
  
    * **Code:** 200 <br />
    **Content:** 
    ```json
    { 
        "success" : true,
        "data": {
            "abbreviation": "RSC",
            "bus_reg_nbr": "10123456789",
            "id": 1,
            "name": "Regional Shire Council"
        }
    }
    ```
 

## Error Responses

  * **Code:** 400 Bad Request <br />
    **Content:** 
    ```json
    {
        "success": false,
        "error_code": 400,
        "message": "The submitted request is invalid and cannot be processed" 
    }
    ```

    OR

  * **Code:** 403 UNAUTHORIZED <br />
    **Content:** 
    ```json
    {
        "success": false,
        "error_code": 403,
        "message": "You are not authorised to perform the request" 
    }
    ```

    OR

  * **Code:** 404 NOT FOUND <br />
    **Content:** 
    ```json
    {
        "success": false,
        "error_code": 404,
        "message": "The resource you requested could not be found" 
    }
    ```

    OR

  * **Code:** 500 Server Error <br />
    **Content:**
    ```json
    {
        "success": false,
        "error_code": 500,
        "message": "An error occurred on the server while trying to process your request" 
    }
    ```
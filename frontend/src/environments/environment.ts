

export const environment = {
  production: false,
  auth: {
    domain: 'car-project-udacity.au.auth0.com',
    clientId: '5GiofyrEGQo3QVEZlt357yEi0LqiWHLP',
    audience: 'car-project-api.hendley.id.au',
    // Specify configuration for the interceptor              
    httpInterceptor: {
      allowedList: [
        'http://localhost:8080/api/*'
      ]
    }
  },
  api: {
    host: 'http://localhost:8080'
  }
};

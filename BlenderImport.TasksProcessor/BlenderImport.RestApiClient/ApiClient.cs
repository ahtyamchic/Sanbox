using System;
using System.Collections.Generic;
using RestSharp;
using TaskRender.RestApiClient.Api;

namespace TaskRender.RestApiClient
{
    public class ApiClient : IApiClient
    {
        private readonly ApiClientConfiguration _configuration;
        private const string API = "render_task";

        public ApiClient(ApiClientConfiguration configuration)
        {
            _configuration = configuration;
        }

        public IEnumerable<RenderTask> GetRenderTasks()
        {
            var request = new RestRequest(BuildResourceString(_configuration.GetAllTaskApiKey), Method.GET);
            return Execute<List<RenderTask>>(request);
        }

        public RenderTaskWithData GetRenderTask(string id)
        {
            var request = new RestRequest(BuildResourceString(_configuration.GetAllTaskApiKey), Method.GET);
            return Execute<RenderTaskWithData>(request);
        }

        public void UpdateRenderTask(string id, string imageBase64)
        {
            var request = new RestRequest(BuildResourceString(_configuration.GetAllTaskApiKey, id), Method.POST);
            request.AddParameter("result", imageBase64);
            
            Execute(request);
        }

        private T Execute<T>(RestRequest request) where T : new()
        {
            var client = CreateRestClient();
            var response = client.Execute<T>(request);

            if (response.ErrorException != null)
            {
                const string message = "Error retrieving response.  Check inner details for more info.";
                var exception = new ApplicationException(message, response.ErrorException);
                throw exception;
            }
            return response.Data;
        }

        private void Execute(RestRequest request)
        {
            var client = CreateRestClient();

            var response = client.Execute(request);

            if (response.ErrorException != null)
            {
                const string message = "Error retrieving response.  Check inner details for more info.";
                var exception = new ApplicationException(message, response.ErrorException);
                throw exception;
            }
        }

        private RestClient CreateRestClient()
        {
            var client = new RestClient();
            client.BaseUrl = new Uri(_configuration.BaseUrl);
            //client.Authenticator = new HttpBasicAuthenticator(_accountSid, _secretKey);
            //request.AddParameter("AccountSid", _accountSid, ParameterType.UrlSegment); // used on every request
            return client;
        }

        private static string BuildResourceString(string apiKey, string id = null)
        {
            return string.IsNullOrEmpty(id)
                ? string.Format("{0}/{1}", API, apiKey)
                : string.Format("{0}/{1}/{2}", API, apiKey, id);
        }
    }
}
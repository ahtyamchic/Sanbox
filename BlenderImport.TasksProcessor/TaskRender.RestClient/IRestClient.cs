using RestSharp;

namespace TaskRender.RestClient
{
    interface IRestClient
    {
        void GetRequest();
        void PostRequest();
    }

    class RestClient : IRestClient
    {
        private readonly string _serverUrl;
        private RestClient _client;

        public RestClient(string serverUrl)
        {
            _serverUrl = serverUrl;
             _client = new RestClient(_serverUrl);
        }

        public void GetRequest(string resource, params object[] args)
        {
            var request = new RestRequest("resource/{id}", Method.GET);
            request.AddParameter("name", "value"); // adds to POST or URL querystring based on Method
            request.AddUrlSegment("id", "123"); // replaces matching token in request.Resource
        }

        public void PostRequest()
        {
            throw new System.NotImplementedException();
        }
    }
}
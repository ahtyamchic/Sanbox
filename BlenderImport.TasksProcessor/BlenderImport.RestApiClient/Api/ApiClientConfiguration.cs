namespace TaskRender.RestApiClient.Api
{
    public class ApiClientConfiguration
    {
        public string BaseUrl { get; set; }
        public string GetAllTaskApiKey { get; set; }
        public string GetTaskByIdApiKey { get; set; }
        public string UpdateTaskApiKey { get; set; }
    }
}
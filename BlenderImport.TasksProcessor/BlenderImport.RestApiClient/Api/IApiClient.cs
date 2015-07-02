using System.Collections.Generic;

namespace TaskRender.RestApiClient.Api
{
    public interface IApiClient
    {
        IEnumerable<RenderTask> GetRenderTasks();
        RenderTaskWithData GetRenderTask(string id);
        void UpdateRenderTask(string id, string imageBase64);
    }
}
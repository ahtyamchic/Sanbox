using System;
using System.IO;
using System.Threading.Tasks;
using TaskRender.RestApiClient.Api;

namespace TaskRender.TasksProcessor
{
    public interface IBlenderClient : IDisposable
    {
        Task ImportAsync(RenderTaskWithData task);
        Task RenderAsync();
        Stream GetRenderedResult();
        void Clear();
    }
}
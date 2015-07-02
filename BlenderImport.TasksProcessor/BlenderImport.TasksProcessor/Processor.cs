using System;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using TaskRender.RestApiClient.Api;

namespace TaskRender.TasksProcessor
{
    public class Processor : ITaskProcessor, IDisposable
    {
        private readonly IBlenderClient _blenderClient;
        private readonly IImageToBase64Convertor _convertor;
        private readonly IApiClient _apiClient;
        private readonly ProcessorConfiguration _configuration;
        private Timer _timer;

        public Processor(IBlenderClient blenderClient,
            IImageToBase64Convertor convertor, 
            IApiClient apiClient,
            ProcessorConfiguration configuration)
        {
            if (blenderClient == null) throw new ArgumentNullException("blenderClient");
            if (convertor == null) throw new ArgumentNullException("convertor");
            if (apiClient == null) throw new ArgumentNullException("apiClient");
            if (configuration == null) throw new ArgumentNullException("configuration");

            _blenderClient = blenderClient;
            _convertor = convertor;
            _apiClient = apiClient;
            _configuration = configuration;
        }

        private void ProcessTasks(object state)
        {
            var availableNewTaskIds =
                _apiClient.GetRenderTasks()
                .Where(t => t.Status == RenderTaskStatus.New)
                .Select(t => t.TaskId);

            foreach (var id in availableNewTaskIds)
            {
                var renderTask = _apiClient.GetRenderTask(id);

                var imageAsBytes = RenderTask(renderTask).Result;
                var imageAsBase64 = _convertor.Convert(new MemoryStream(imageAsBytes));

                _apiClient.UpdateRenderTask(id, imageAsBase64);
            }
        }

        private async Task<byte[]> RenderTask(RenderTaskWithData renderTask)
        {
            // TODO: add error handling!!!!!!!
 
            await _blenderClient.ImportAsync(renderTask);
            await _blenderClient.RenderAsync();

            var image = _blenderClient.GetRenderedResult();
            var buff = new byte[image.Length];
            await image.ReadAsync(buff, buff.Length, 0);
            _blenderClient.Clear();

            return buff;
        }

        public void Start()
        {
            _timer = new Timer(ProcessTasks, null,
               TimeSpan.FromSeconds(_configuration.DelayBeforeProcessorStart),
               TimeSpan.FromSeconds(_configuration.Interval));
        }

        public void Stop()
        {
            _timer.Change(0, 0);
        }

        public void Dispose()
        {
            Stop();
            _timer.Dispose();
        }
    }
}

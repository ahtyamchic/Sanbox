using System.IO;

namespace TaskRender.TasksProcessor
{
    public interface IImageToBase64Convertor
    {
        string Convert(Stream image);
    }
}
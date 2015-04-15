using System.Diagnostics;
using System.IO;

namespace BlenderScriptRunner
{
    public class Runner
    {
        private readonly string _defaulBlenderLocation = "c:\\Program Files\\Blender Foundation\\Blender\\blender.exe";
        private readonly string _blenderCmdArgPattern = @" -ba {0} --python {1} -- {2} {3}";
        public void Run(Config cfg)
        {
            string blenderLocation = string.IsNullOrEmpty(cfg.BlenderPath) ? _defaulBlenderLocation : cfg.BlenderPath;

            string cmdArg = string.Format(_blenderCmdArgPattern, "EmptyScene.blend", "importJson.py", cfg.JsonPath, string.Format("{0}\\", cfg.TempPath));
            Process.Start(blenderLocation, cmdArg);
        }

        public string DefaultBlenderLocation
        {
            get { return _defaulBlenderLocation; }
        }
    }
}
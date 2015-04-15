using System;
using System.Drawing;
using System.IO;
using System.Windows.Forms;
using BlenderScriptRunner;

namespace ScriptRunner
{
    public partial class FormUi : Form
    {
        private readonly Runner _runner;
        private Config _cfg;

        public FormUi()
        {
            InitializeComponent();

            _runner = new Runner();
            _cfg = new Config();

            BlenderDirTextBox.ReadOnly = true;
            BlenderDirTextBox.TextChanged += (o, s) => _cfg.BlenderPath = BlenderDirTextBox.Text;
            WarnLabel(BlendeLabel);

            JsonTextBox.ReadOnly = true;
            JsonTextBox.TextChanged += (o, s) => _cfg.JsonPath = JsonTextBox.Text;
            WarnLabel(JsonLabel);

            TempDirTextBox.ReadOnly = true;
            TempDirTextBox.TextChanged += (o, s) => _cfg.TempPath = TempDirTextBox.Text;
            WarnLabel(TempLabel);

            if (File.Exists(_runner.DefaultBlenderLocation))
            {
                _cfg.BlenderPath = _runner.DefaultBlenderLocation;
                BlenderDirTextBox.Text = _cfg.BlenderPath;
                WarnLabel(BlendeLabel, false);
            }

            RunButton.Enabled = false;
        }

        private bool CanRun()
        {
            return !IsWarn(BlendeLabel) && !IsWarn(JsonLabel) && !IsWarn(TempLabel);
        }

        private void WarnLabel(Label label, bool isWarn = true)
        {
            label.ForeColor = isWarn ? Color.Red : Color.Black;
        }

        private bool IsWarn(Label label)
        {
            return label.ForeColor == Color.Red;
        }

        private void BlenderBrowseButton_Click(object sender, EventArgs e)
        {
            SelectFile("Select blender.exe", BlenderDirTextBox, BlendeLabel, "Application files(.exe)|*.exe");
            AllowRunScript();
        }

        private void SelectFile(string selectFile, TextBox textBox, Label label, string filter = null)
        {
            var dialog = new OpenFileDialog();
            dialog.Title = selectFile;
            dialog.Filter = filter;
            if (dialog.ShowDialog() == DialogResult.OK && File.Exists(dialog.FileName))
            {
                string fileName = dialog.FileName;
                textBox.Text = fileName;
                WarnLabel(label, false);
            }
        }

        private void JsonButton_Click(object sender, EventArgs e)
        {
            SelectFile("Select json file", JsonTextBox, JsonLabel, "Json files(.json)|*.json");
            AllowRunScript();
        }

        private void TempDirButton_Click(object sender, EventArgs e)
        {
            var dirDialog = new FolderBrowserDialog();
            dirDialog.Description = "Select temp directory";
            dirDialog.ShowNewFolderButton = true;
            if (dirDialog.ShowDialog() == DialogResult.OK && Directory.Exists(dirDialog.SelectedPath))
            {
                TempDirTextBox.Text = dirDialog.SelectedPath;
                WarnLabel(TempLabel, false);
                AllowRunScript();
            }
        }

        private void AllowRunScript()
        {
            if (CanRun()) RunButton.Enabled = true;
        }

        private void RunButton_Click(object sender, EventArgs e)
        {
            try
            {
                _runner.Run(_cfg);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Unexpected error occured. \n Details:" + ex, "Oops", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}

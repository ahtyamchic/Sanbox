namespace ScriptRunner
{
    partial class FormUi
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.RunButton = new System.Windows.Forms.Button();
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.BlenderDirTextBox = new System.Windows.Forms.TextBox();
            this.JsonTextBox = new System.Windows.Forms.TextBox();
            this.TempDirTextBox = new System.Windows.Forms.TextBox();
            this.BlendeLabel = new System.Windows.Forms.Label();
            this.JsonLabel = new System.Windows.Forms.Label();
            this.TempLabel = new System.Windows.Forms.Label();
            this.BlenderBrowseButton = new System.Windows.Forms.Button();
            this.JsonButton = new System.Windows.Forms.Button();
            this.TempDirButton = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // RunButton
            // 
            this.RunButton.Location = new System.Drawing.Point(905, 281);
            this.RunButton.Name = "RunButton";
            this.RunButton.Size = new System.Drawing.Size(166, 43);
            this.RunButton.TabIndex = 0;
            this.RunButton.Text = "Run";
            this.RunButton.UseVisualStyleBackColor = true;
            this.RunButton.Click += new System.EventHandler(this.RunButton_Click);
            // 
            // menuStrip1
            // 
            this.menuStrip1.ImageScalingSize = new System.Drawing.Size(32, 32);
            this.menuStrip1.Location = new System.Drawing.Point(0, 0);
            this.menuStrip1.Name = "menuStrip1";
            this.menuStrip1.Size = new System.Drawing.Size(1086, 24);
            this.menuStrip1.TabIndex = 1;
            this.menuStrip1.Text = "menuStrip1";
            // 
            // BlenderDirTextBox
            // 
            this.BlenderDirTextBox.Location = new System.Drawing.Point(219, 82);
            this.BlenderDirTextBox.Name = "BlenderDirTextBox";
            this.BlenderDirTextBox.Size = new System.Drawing.Size(668, 31);
            this.BlenderDirTextBox.TabIndex = 2;
            // 
            // JsonTextBox
            // 
            this.JsonTextBox.Location = new System.Drawing.Point(219, 143);
            this.JsonTextBox.Name = "JsonTextBox";
            this.JsonTextBox.Size = new System.Drawing.Size(668, 31);
            this.JsonTextBox.TabIndex = 3;
            // 
            // TempDirTextBox
            // 
            this.TempDirTextBox.Location = new System.Drawing.Point(219, 205);
            this.TempDirTextBox.Name = "TempDirTextBox";
            this.TempDirTextBox.Size = new System.Drawing.Size(668, 31);
            this.TempDirTextBox.TabIndex = 4;
            // 
            // BlendeLabel
            // 
            this.BlendeLabel.AutoSize = true;
            this.BlendeLabel.Location = new System.Drawing.Point(35, 87);
            this.BlendeLabel.Name = "BlendeLabel";
            this.BlendeLabel.Size = new System.Drawing.Size(175, 25);
            this.BlendeLabel.TabIndex = 5;
            this.BlendeLabel.Text = "Blender directory";
            // 
            // JsonLabel
            // 
            this.JsonLabel.AutoSize = true;
            this.JsonLabel.Location = new System.Drawing.Point(35, 143);
            this.JsonLabel.Name = "JsonLabel";
            this.JsonLabel.Size = new System.Drawing.Size(102, 25);
            this.JsonLabel.TabIndex = 6;
            this.JsonLabel.Text = "JSON file";
            // 
            // TempLabel
            // 
            this.TempLabel.AutoSize = true;
            this.TempLabel.Location = new System.Drawing.Point(35, 205);
            this.TempLabel.Name = "TempLabel";
            this.TempLabel.Size = new System.Drawing.Size(155, 25);
            this.TempLabel.TabIndex = 7;
            this.TempLabel.Text = "Temp directory";
            // 
            // BlenderBrowseButton
            // 
            this.BlenderBrowseButton.Location = new System.Drawing.Point(908, 76);
            this.BlenderBrowseButton.Name = "BlenderBrowseButton";
            this.BlenderBrowseButton.Size = new System.Drawing.Size(166, 43);
            this.BlenderBrowseButton.TabIndex = 8;
            this.BlenderBrowseButton.Text = "Browse";
            this.BlenderBrowseButton.UseVisualStyleBackColor = true;
            this.BlenderBrowseButton.Click += new System.EventHandler(this.BlenderBrowseButton_Click);
            // 
            // JsonButton
            // 
            this.JsonButton.Location = new System.Drawing.Point(908, 138);
            this.JsonButton.Name = "JsonButton";
            this.JsonButton.Size = new System.Drawing.Size(166, 43);
            this.JsonButton.TabIndex = 9;
            this.JsonButton.Text = "Browse";
            this.JsonButton.UseVisualStyleBackColor = true;
            this.JsonButton.Click += new System.EventHandler(this.JsonButton_Click);
            // 
            // TempDirButton
            // 
            this.TempDirButton.Location = new System.Drawing.Point(908, 201);
            this.TempDirButton.Name = "TempDirButton";
            this.TempDirButton.Size = new System.Drawing.Size(166, 43);
            this.TempDirButton.TabIndex = 10;
            this.TempDirButton.Text = "Browse";
            this.TempDirButton.UseVisualStyleBackColor = true;
            this.TempDirButton.Click += new System.EventHandler(this.TempDirButton_Click);
            // 
            // FormUi
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(12F, 25F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1086, 387);
            this.Controls.Add(this.TempDirButton);
            this.Controls.Add(this.JsonButton);
            this.Controls.Add(this.BlenderBrowseButton);
            this.Controls.Add(this.TempLabel);
            this.Controls.Add(this.JsonLabel);
            this.Controls.Add(this.BlendeLabel);
            this.Controls.Add(this.TempDirTextBox);
            this.Controls.Add(this.JsonTextBox);
            this.Controls.Add(this.BlenderDirTextBox);
            this.Controls.Add(this.RunButton);
            this.Controls.Add(this.menuStrip1);
            this.MainMenuStrip = this.menuStrip1;
            this.Name = "FormUi";
            this.Text = "Blender script runner";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button RunButton;
        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.TextBox BlenderDirTextBox;
        private System.Windows.Forms.TextBox JsonTextBox;
        private System.Windows.Forms.TextBox TempDirTextBox;
        private System.Windows.Forms.Label BlendeLabel;
        private System.Windows.Forms.Label JsonLabel;
        private System.Windows.Forms.Label TempLabel;
        private System.Windows.Forms.Button BlenderBrowseButton;
        private System.Windows.Forms.Button JsonButton;
        private System.Windows.Forms.Button TempDirButton;
    }
}


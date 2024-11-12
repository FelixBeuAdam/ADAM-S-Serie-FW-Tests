import sys, clr 

clr.AddReference("System.Drawing")              
clr.AddReference("System.Windows.Forms")

# Add a reference to the APx API        
clr.AddReference(r"C:\\Program Files\\Audio Precision\\APx500 8.1\\API\\AudioPrecision.API2.dll")    
clr.AddReference(r"C:\\Program Files\\Audio Precision\\APx500 8.1\\API\\AudioPrecision.API.dll") 

from AudioPrecision.API import *
from System.Drawing import Point
from System.Windows.Forms import Application, Button, Form, Label
from System.IO import Directory, Path

class Container(Form):

    def __init__(self): # Create a form with a label and four buttons
        super().__init__()
        self.Text = 'APx Python Example'
        self.Height = 280
        self.Width = 200
        
        self.label = Label()
        self.label.Text = "Python APx Control"
        self.label.Location = Point(20, 20)
        self.label.Height = 20
        self.label.Width = 200

        self.count = 0

        bLoad = Button()
        bLoad.Text = "Load APx Software"
        bLoad.Location = Point(20, 50)
        bLoad.Width = 150
        bLoad.Click += self.APxLoad

        bProj = Button()
        bProj.Text = "Open Sample Project"
        bProj.Location = Point(20, 80)
        bProj.Width = 150
        bProj.Click += self.APxProject
        
        bSignalPath = Button()
        bSignalPath.Text = "Configure Signal Path"
        bSignalPath.Location = Point(20, 110)
        bSignalPath.Width = 150
        bSignalPath.Click += self.APxSignalPath
        
        bAddMeas = Button()
        bAddMeas.Text = "Add Measurement"
        bAddMeas.Location = Point(20, 140)
        bAddMeas.Width = 150
        bAddMeas.Click += self.APxAddMeasurement

        bMeas = Button()
        bMeas.Text = "Run Sequence..."
        bMeas.Location = Point(20, 170)
        bMeas.Width = 150
        bMeas.Click += self.APxRunSequence

        bData = Button()
        bData.Text = "Get Data"
        bData.Location = Point(20, 200)
        bData.Width = 150
        bData.Click += self.APxGetData

        self.Controls.Add(self.label)
        self.Controls.Add(bLoad)
        self.Controls.Add(bProj)
        self.Controls.Add(bSignalPath)
        self.Controls.Add(bAddMeas)
        self.Controls.Add(bMeas)    
        self.Controls.Add(bData)    

    def APxLoad(self, sender, args): # Initialize the software and set it to Visible
        APx = APx500_Application()
        APx.Visible = True
    
    def APxProject(self, sender, args): # Load the example project file
        filename = "SampleProject.approjx"
        directory = Directory.GetCurrentDirectory()
        fullpath = Path.Combine(directory, filename)
        APx = APx500_Application()
        APx.OpenProject(fullpath)
    
    def APxSignalPath(self, sender, args): # Run the sequence, which will run the Frequency Response measurement
        APx = APx500_Application()
        APx.SignalPathSetup.OutputConnector.Type = OutputConnectorType.AnalogBalanced
        APx.SignalPathSetup.InputConnector.Type = InputConnectorType.AnalogBalanced 
        APx.SignalPathSetup.Measure = MeasurandType.Acoustic
        input1 = APx.SignalPathSetup.InputSettings(APxInputSelection.Input1)
        input1.Channels[0].Name = "Mic"
        input1.Channels[0].Sensitivity.Value = 0.011
    
    def APxAddMeasurement(self, sender, args): # Run the sequence, which will run the Frequency Response measurement
        APx = APx500_Application()
        APx.AddMeasurement("Signal Path1", MeasurementType.AcousticResponse)
        APx.AcousticResponse.GeneratorWithPilot.Frequencies.Start.Value = 100;
        APx.AcousticResponse.GeneratorWithPilot.Frequencies.Stop.Value = 10000;
        APx.AcousticResponse.GeneratorWithPilot.Levels.Sweep.SetValue(OutputChannelIndex.Ch1, "1 Vrms");
        APx.AcousticResponse.GeneratorWithPilot.Durations.Sweep.Value = 1;
        
        #Check a couple results to be included in the active sequence
        APx.AcousticResponse.Phase.Checked = True
        APx.AcousticResponse.ThdRatio.Checked = True
        
        #Add a derived result and configure it
        smooth = APx.AcousticResponse.Level.AddDerivedResult(MeasurementResultType.Smooth).Result.AsSmoothResult();
        smooth.OctaveSmoothing = OctaveSmoothingType.Octave3
        smooth.Name = "Smoothed Response"
        smooth.Checked = True
        
        #Add an export data sequence step to automatically export the smoothed data when the measurement is run in a sequence.
        exportStep = APx.AcousticResponse.SequenceMeasurement.SequenceSteps.ExportResultDataSteps.Add()
        exportStep.ResultName = smooth.Name
        exportStep.ExportSpecification = "All Points"
        exportStep.FileName = "$(MyDocuments)\\SmoothedResponse.xlsx"
        exportStep.Append = False
        
    def APxRunSequence(self, sender, args): # Run the sequence, which will run the Frequency Response measurement
        APx = APx500_Application()
        APx.Sequence.Run()
      
    def APxGetData(self, sender, args): # Get results acquired in the last sequence run
        APx = APx500_Application()

        # Get Frequency Response RMS Level XY values by result name (string)
        level_xvalues = APx.Sequence[0]["Acoustic Response"].SequenceResults["Smoothed Response"].GetXValues(InputChannelIndex.Ch1, VerticalAxis.Left, SourceDataType.Measured, 1)
        level_yvalues = APx.Sequence[0]["Acoustic Response"].SequenceResults["Smoothed Response"].GetYValues(InputChannelIndex.Ch1, VerticalAxis.Left, SourceDataType.Measured, 1)

         # Get Frequency Response Gain XY values by result type
        thd_xvalues = APx.Sequence[0]["Acoustic Response"].SequenceResults[MeasurementResultType.ThdRatioVsFrequency].GetXValues(InputChannelIndex.Ch1, VerticalAxis.Left, SourceDataType.Measured, 1)
        thd_yvalues = APx.Sequence[0]["Acoustic Response"].SequenceResults[MeasurementResultType.ThdRatioVsFrequency].GetYValues(InputChannelIndex.Ch1, VerticalAxis.Left, SourceDataType.Measured, 1)

form = Container()
Application.Run(form)

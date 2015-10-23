import FWCore.ParameterSet.Config as cms

process = cms.Process("TagProbe")
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.destinations = ['cout', 'cerr']
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

################################################
##                      _              _       
##   ___ ___  _ __  ___| |_ __ _ _ __ | |_ ___ 
##  / __/ _ \| '_ \/ __| __/ _` | '_ \| __/ __|
## | (_| (_) | | | \__ \ || (_| | | | | |_\__ \
##  \___\___/|_| |_|___/\__\__,_|_| |_|\__|___/
##                                              
################################################

InputFileName = "/afs/cern.ch/work/f/ffacchin/public/Formatted_DYLL_all.root"  
OutputFilePrefix = "PTratio-mc" 
PDFName = "pdfSignalPlusBackground"

################################################
#specifies the binning of parameters
#EfficiencyBins = cms.PSet(probe_pt = cms.vdouble( 20, 40, 60, 100, 200, 500 ),
#                          probe_absEta = cms.vdouble( 0.0, 1.5),     
#                          )     
EfficiencyBins = cms.PSet(probe_pt = cms.vdouble( 0, 100, 200, 300, 400, 500 ),
                          probe_absEta = cms.vdouble( 0.0, 1.5),     
                          )     

EfficiencyBinningSpecificationMC = cms.PSet(
    UnbinnedVariables = cms.vstring("pt_ratio", "weight"),
    BinnedVariables = cms.PSet(EfficiencyBins,
                               ),
    BinToPDFmap = cms.vstring(PDFName)  
)

############################################################################################

mcTruthModules = cms.PSet(
    MCtruth_Tight = cms.PSet(EfficiencyBinningSpecificationMC,
                             EfficiencyCategoryAndState = cms.vstring("probe_fullsel", "pass"),
                             ),
    )

############################################################################################
############################################################################################
####### GsfElectron->Id / selection efficiency 
############################################################################################
############################################################################################

process.GsfElectronToId = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
                                         InputFileNames = cms.vstring(InputFileName),
                                         InputDirectoryName = cms.string("tnpAna"),
                                         InputTreeName = cms.string("TaPTree"), 
                                         OutputFileName = cms.string(OutputFilePrefix+"FullSel.root"),
                                         NumCPU = cms.uint32(1),
                                         SaveWorkspace = cms.bool(False), 
                                         doCutAndCount = cms.bool(True),
                                         floatShapeParameters = cms.bool(True),
                                         binnedFit = cms.bool(True),
                                         binsForFit = cms.uint32(40),
                                         WeightVariable = cms.string("weight"),
                                         
                                         # defines all the real variables of the probes available in the input tree and intended for use in the efficiencies
                                         Variables = cms.PSet(pt_ratio = cms.vstring("Tag-Probe Pt_ratio", "0.0", "10.0", "GeV/c^{2}"),
                                                              probe_pt = cms.vstring("Probe E_{T}", "0", "500", "GeV/c"), 
                                                              probe_absEta = cms.vstring("Probe #eta", "0", "2.5", ""),   
                                                              weight = cms.vstring("Total weight", "0", "100", ""),
                                                              ),

                                         # defines all the discrete variables of the probes available in the input tree and intended for use in the efficiency calculations
                                         Categories = cms.PSet(probe_fullsel = cms.vstring("probe_fullsel", "dummy[pass=1,fail=0]"),
                                                               
                                                               ),

                                         # defines all the PDFs that will be available for the efficiency calculations; 
                                         PDFs = cms.PSet(pdfSignalPlusBackground = cms.vstring(
            "RooGaussian::signalResPass(pt_ratio, meanP[.0,-5.000,5.000],sigmaP[0.956,0.00,5.000])",
            "RooGaussian::signalResFail(pt_ratio, meanF[.0,-5.000,5.000],sigmaF[0.956,0.00,5.000])",
            "ZGeneratorLineShape::signalPhyPass(pt_ratio,\"/afs/cern.ch/work/f/ffacchin/public/MCtemplates.root\", \"hPt_Ratio_0.000000To100.000000_0.000000To1.500000_Pass\")",
            "ZGeneratorLineShape::signalPhyPass(pt_ratio,\"/afs/cern.ch/work/f/ffacchin/public/MCtemplates.root\", \"hPt_Ratio_100.000000To200.000000_0.000000To1.500000_Pass\")",
            "ZGeneratorLineShape::signalPhyPass(pt_ratio,\"/afs/cern.ch/work/f/ffacchin/public/MCtemplates.root\", \"hPt_Ratio_200.000000To300.000000_0.000000To1.500000_Pass\")",
            "ZGeneratorLineShape::signalPhyPass(pt_ratio,\"/afs/cern.ch/work/f/ffacchin/public/MCtemplates.root\", \"hPt_Ratio_300.000000To400.000000_0.000000To1.500000_Pass\")",
            "ZGeneratorLineShape::signalPhyFail(pt_ratio,\"/afs/cern.ch/work/f/ffacchin/public/MCtemplates.root\", \"hPt_Ratio_400.000000To500.000000_0.000000To1.500000_Fail\")",
            "RooCMSShape::backgroundPass(pt_ratio, alphaPass[60.,50.,70.], betaPass[0.001, 0.,0.1], gammaPass[0.1, 0, 1], peakPass[90.0])",
            "RooCMSShape::backgroundFail(pt_ratio, alphaFail[60.,50.,70.], betaFail[0.001, 0.,0.1], gammaFail[0.1, 0, 1], peakFail[90.0])",
            "FCONV::signalPass(pt_ratio, signalPhyPass, signalResPass)",
            "FCONV::signalFail(pt_ratio, signalPhyFail, signalResFail)",     
            "efficiency[0.5,0,1]",
            "signalFractionInPassing[1.0]"     
            ),
                                                         ),

                                         Efficiencies = cms.PSet(mcTruthModules,
                                                                 )
                                         )

process.fit = cms.Path(
    process.GsfElectronToId  
    )

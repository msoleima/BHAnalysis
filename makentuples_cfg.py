import FWCore.ParameterSet.Config as cms
process = cms.Process('ANA')
process.load('PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.Geometry_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag.globaltag = 'PHYS14_25_V1'
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(100))
process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1

process.TFileService=cms.Service("TFileService",
	fileName=cms.string("ntuple_output.root"),
	closeFileFast = cms.untracked.bool(True)
)
process.options = cms.untracked.PSet(
	allowUnscheduled = cms.untracked.bool(True),
	wantSummary = cms.untracked.bool(False),
)
process.out = cms.OutputModule('PoolOutputModule',
	fileName = cms.untracked.string('edm_output.root'),
	outputCommands = cms.untracked.vstring('keep *')
)
process.source = cms.Source("PoolSource",
	fileNames = cms.untracked.vstring('root://eoscms//eos/cms/store/mc/Phys14DR/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/MINIAODSIM/PU20bx25_PHYS14_25_V1-v1/00000/FE26BEB8-D575-E411-A13E-00266CF2AE10.root')
)


#
# START ELECTRON ID SECTION
#
# Set up everything that is needed to compute electron IDs and
# add the ValueMaps with ID decisions into the event data stream
#
# Load tools and function definitions
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
process.load("RecoEgamma.ElectronIdentification.egmGsfElectronIDs_cfi")
# overwrite a default parameter: for miniAOD, the collection name is a slimmed one
process.egmGsfElectronIDs.physicsObjectSrc = cms.InputTag('slimmedElectrons')
from PhysicsTools.SelectorUtils.centralIDRegistry import central_id_registry
process.egmGsfElectronIDSequence = cms.Sequence(process.egmGsfElectronIDs)
# Define which IDs we want to produce
# Each of these two example IDs contains all four standard
# cut-based ID working points (only two WP of the PU20bx25 are actually used here).
my_id_modules = ['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_PHYS14_PU20bx25_V1_miniAOD_cff']
#Add them to the VID producer
for idmod in my_id_modules:
	setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)
# Do not forget to add the egmGsfElectronIDSequence to the path,
# as in the example below!
#
# END ELECTRON ID SECTION
#
#
# Configure an example module for user analysis of electrons
#

process.bhana = cms.EDAnalyzer('BHAnalyzerTLBSM',
	electronTag = cms.InputTag("slimmedElectrons"),
	muonTag = cms.untracked.InputTag("slimmedMuons"),
	jetTag = cms.untracked.InputTag("slimmedJets"),
	tauTag = cms.untracked.InputTag("slimmedTaus"),
	metTag = cms.untracked.InputTag("slimmedMETs"),
	photonTag = cms.untracked.InputTag("slimmedPhotons"),
	ebRecHitTag = cms.untracked.InputTag("reducedEgamma", "reducedEBRecHits"),
	eeRecHitTag = cms.untracked.InputTag("reducedEgamma", "reducedEERecHits"),
	primaryVertex = cms.untracked.InputTag("offlineSlimmedPrimaryVertices"),
	triggerTag = cms.untracked.InputTag("TriggerResults"),
	MCLabel = cms.untracked.bool(False),
	electronIdMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-medium")
)
process.p = cms.Path(
	process.bhana
) 
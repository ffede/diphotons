#define templateMaker_cxx
#include "templateMaker.h"
#include <iostream>
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>

using namespace std;

#define ptBinsEB 5
#define ptBinsEE 5


#define etaBinsEB 1
#define etaBinsEE 1


void templateMaker::Loop()
{
  if (fChain == 0) return;
  
  float ptInfEB[ptBinsEB] = {0.,100.,200.,300.,400.};
  float ptSupEB[ptBinsEB] = {100.,200.,300.,400.,500.};
  float ptInfEE[ptBinsEE] = {0.,100.,200.,300.,400.};
  float ptSupEE[ptBinsEE] = {100.,200.,300.,400.,500.};
  
  /*
  float ptInfEB[1] = {0.};
  float ptSupEB[1] = {500.};
  float ptInfEE[1] = {0.};
  float ptSupEE[1] = {500.};
  */
  float etaInfEB[1] = {0.0};
  float etaSupEB[1] = {1.5};
  float etaInfEE[1] = {1.5};
  float etaSupEE[1] = {2.5};


  // histos for passing and failing probes     
  TH1F *hPt_RatioEBpass[ptBinsEB][etaBinsEB], *hPt_RatioEEpass[ptBinsEE][etaBinsEE];
  TH1F *hPt_RatioEBfail[ptBinsEB][etaBinsEB], *hPt_RatioEEfail[ptBinsEE][etaBinsEE];
  
  for (int ii=0; ii<ptBinsEB; ii++) {
    for (int jj=0; jj<etaBinsEB; jj++) {
      hPt_RatioEBpass[ii][jj] = new TH1F("hPt_RatioEBpass[ii][jj]","hPt_RatioEBpass[ii][jj]",80,0.0,10);
      hPt_RatioEBpass[ii][jj]->Sumw2();
      hPt_RatioEBfail[ii][jj] = new TH1F("hPt_RatioEBfail[ii][jj]","hPt_RatioEBfail[ii][jj]",80,0.0,10);
      hPt_RatioEBfail[ii][jj]->Sumw2();
    }
  }
  for (int ii=0; ii<ptBinsEE; ii++) {
      for (int jj=0; jj<etaBinsEE; jj++) {
	hPt_RatioEEpass[ii][jj] = new TH1F("hPt_RatioEEpass[ii][jj]","hPt_RatioEEpass[ii][jj]",80,0.0,10);
	hPt_RatioEEpass[ii][jj]->Sumw2();
	hPt_RatioEEfail[ii][jj] = new TH1F("hPt_RatioEEfail[ii][jj]","hPt_RatioEEfail[ii][jj]",80,0.0,10);
	hPt_RatioEEfail[ii][jj]->Sumw2();
      }
  }
  
  
  // Loop over entries    
  Long64_t nentries = fChain->GetEntriesFast();
  Long64_t nbytes = 0, nb = 0;
  cout << "Running over " << nentries << " events" << endl;

  for (Long64_t jentry=0; jentry<nentries;jentry++) {
    Long64_t ientry = LoadTree(jentry);
    if (ientry < 0) break;
    nb = fChain->GetEntry(jentry);   nbytes += nb;
    if(jentry%10000==0) cout << jentry << endl;
        
    // passed or not 
    bool passed = false;
    if (probe_fullsel) passed = true;

    for (int ii=0; ii<ptBinsEB; ii++) {
      for (int jj=0; jj<etaBinsEB; jj++) {
	if (probe_absEta>=etaInfEB[jj] && probe_absEta<=etaSupEB[jj]){ 
	  if (probe_pt>=ptInfEB[ii] && probe_pt<=ptSupEB[ii]) { 
	    if (passed) hPt_RatioEBpass[ii][jj]->Fill(pt_ratio);
	    else hPt_RatioEBfail[ii][jj]->Fill(pt_ratio); 
	  }
	}
      }
    }

    for (int ii=0; ii<ptBinsEE; ii++) {
      for (int jj=0; jj<etaBinsEE; jj++) {
	if (probe_absEta>=etaInfEE[jj] && probe_absEta<=etaSupEE[jj]){ 
	  if (probe_pt>=ptInfEE[ii] && probe_pt<=ptSupEE[ii]) { 
	    if (passed) hPt_RatioEEpass[ii][jj]->Fill(pt_ratio);
	    else hPt_RatioEEfail[ii][jj]->Fill(pt_ratio); 
	  }
	}
      }
    }
    
  }  // Loop over entries
    


  // saving histos
  TFile myFileTemp("MCtemplates.root","RECREATE");
  
  for (int ii=0; ii<ptBinsEB; ii++) {
    for (int jj=0; jj<etaBinsEB; jj++) {
      TString thisName;
      thisName = TString::Format("hPt_Ratio_%f",ptInfEB[ii])+TString::Format("To%f",ptSupEB[ii])+TString::Format("_%f",etaInfEB[jj])+TString::Format("To%f",etaSupEB[jj])+"_Pass";
      hPt_RatioEBpass[ii][jj] ->Write(thisName);
      thisName = TString::Format("hPt_Ratio_%f",ptInfEB[ii])+TString::Format("To%f",ptSupEB[ii])+TString::Format("_%f",etaInfEB[jj])+TString::Format("To%f",etaSupEB[jj])+"_Fail";
      hPt_RatioEBfail[ii][jj] ->Write(thisName);
    }
  }
  
  for (int ii=0; ii<ptBinsEE; ii++) {
    for (int jj=0; jj<etaBinsEE; jj++) {
      TString thisName;
      thisName = TString::Format("hPt_Ratio_%f",ptInfEE[ii])+TString::Format("To%f",ptSupEE[ii])+TString::Format("_%f",etaInfEE[jj])+TString::Format("To%f",etaSupEE[jj])+"_Pass";
      hPt_RatioEEpass[ii][jj] ->Write(thisName);
      thisName = TString::Format("hPt_Ratio_%f",ptInfEE[ii])+TString::Format("To%f",ptSupEE[ii])+TString::Format("_%f",etaInfEE[jj])+TString::Format("To%f",etaSupEE[jj])+"_Fail";
      hPt_RatioEEfail[ii][jj] ->Write(thisName);
    }
  }
}

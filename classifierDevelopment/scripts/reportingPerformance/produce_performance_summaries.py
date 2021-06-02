# Import packages
import pandas as pd 
from accelerometer import accClassification # Note should use loaded version of this 
from datetime import date
import sklearn.metrics as metrics

# Set up date for recording
today = date.today()
rec_date = today.strftime("%Y-%m-%d")

# Set up filestem
overall = "/well/doherty/users/llz512/home/paperRW2021/classifierDevelopment/inputData/processingFollowingSep20Protocols/"
overall_out = "/well/doherty/users/llz512/home/paperRW2021/classifierDevelopment/plots/"

# Read in files
dDem = pd.read_csv(overall + "c24-participant-info.csv") 

dClassic = pd.read_csv(overall + "predictions/sep20_LOO_results.csv") 
d38Plus = pd.read_csv(overall + "predictions/may21_restrictedToOver38s.csv")

# Get only older ids 
pids = dDem["pid"][dDem["age"] >=38]
dReportingRest = dClassic[dClassic["participant"].isin(pids)]

# Print participant numbers
print(len(dClassic["participant"].unique))
print(len(dReportingRest["participant"].unique))
print(len(d38Plus["participant"].unique))

# Report 
perParticipantSummaryHTML(dClassic, "label", "predicted", "participant", overall_out + rec_date + "_overall_summary.html")
perParticipantSummaryHTML(dReportingRest, "label", "predicted", "participant", overall_out + rec_date + "_restricted_reporting_summary.html")
perParticipantSummaryHTML(d38Plus, "label", "predicted", "participant", overall_out + rec_date + "_restricted_training_summary.html")


# Also do comparison with overall precision and recall using cutpoint
dTraining = pd.read_csv(overall + "training_data/sep20-c24-modvig-light-sed-sleep.csv") 
dTraining["predicted_by_cutpoint"] = "nonMVPA"
dTraining["predicted_by_cutpoint"][d["enmoTrunc"] > 0.1] = "MVPA" 
dTraining["label_twoway"] = "nonMVPA"
dTraining["label_twoway"][dTraining["label"] == "MVPA"] = "MVPA"

perParticipantSummaryHTML(dTraining, "label_twoway", "predicted_by_cutpoint", "participant", overall_out + rec_date + "_cutpoint_summary.html")
print(metrics.classification_report(dTraining["label_twoway"], dTraining["predicted_by_cutpoint"]))


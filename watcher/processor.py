import pandas as pd


def process_file(video_file):
  """
  Process a video file into a dataframe
  """
  # Read metadata
  metadata = {"length": "160"}
  df = pd.DataFrame(data=metadata, index=[video_file])
  return df

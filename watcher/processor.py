import uuid

import ffmpeg as ff
import pandas as pd


def process_file(video_file):
  """
  Process a video file into a dataframe
  """
  # Read metadata
  params = ff.probe(video_file)
  format = params["format"]

  ## Get interesting data
  start_time = format["start_time"]
  duration = format["duration"]
  end_time = float(start_time) + float(duration)

  metadata = {"start_start":start_time,
	      "duration":duration,
    	      "end_time":end_time,
	      "file":video_file
	     }
  df = pd.DataFrame(data=metadata, index=[video_file])
  return df

def files_to_xml(df):
  """
  Convert dataframe into XML
  """

  def row_xml(row):
    """
    Create a new row
    """
    xml = []
    for i, col_name in enumerate(row.index):
	    xml.append("<File uuid={} path={}>".format(uuid4.uuid4(), row["file"]))
    return xml

  res = '\n'.join(df.apply(row_xml, axis=1))
  return res

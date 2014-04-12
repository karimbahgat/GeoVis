import sys
sys.path.append(r"C:\Users\BIGKIMO\Dropbox\Work\Research\Software\Various Python Libraries\GitDoc")
import gitdoc

FILENAME = "geovis"
FOLDERPATH = r"C:\Users\BIGKIMO\Documents\GitHub\geovis"
OUTPATH = r"C:\Users\BIGKIMO\Documents\GitHub\geovis"
OUTNAME = "USER_MANUAL"
EXCLUDETYPES = ["module","variable"]
gitdoc.Module2GitDown(FOLDERPATH,filename=FILENAME,outputfolder=OUTPATH,outputname=OUTNAME,excludetypes=EXCLUDETYPES)

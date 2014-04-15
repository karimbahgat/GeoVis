import sys
sys.path.append(r"C:\Users\BIGKIMO\Documents\GitHub\GitDoc")
import gitdoc

FILENAME = "geovis"
FOLDERPATH = r"C:\Users\BIGKIMO\Documents\GitHub\geovis"
OUTPATH = r"C:\Users\BIGKIMO\Documents\GitHub\geovis"
OUTNAME = "USER_MANUAL"
EXCLUDETYPES = ["module","variable"]
gitdoc.DocumentModule(FOLDERPATH,filename=FILENAME,outputfolder=OUTPATH,outputname=OUTNAME,excludetypes=EXCLUDETYPES)

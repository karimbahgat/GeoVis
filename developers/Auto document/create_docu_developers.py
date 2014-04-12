import sys
sys.path.append(r"C:\Users\BIGKIMO\Dropbox\Work\Research\Software\Various Python Libraries\GitDoc")
import gitdoc

FILENAME = "geovis"
FOLDERPATH = r"C:\Users\BIGKIMO\Documents\GitHub\geovis"
OUTPATH = r"C:\Users\BIGKIMO\Documents\GitHub\geovis\developers"
OUTNAME = "dev_documentation"
EXCLUDETYPES = ["module"]
gitdoc.Module2GitDown(FOLDERPATH,
                  filename=FILENAME,
                  outputfolder=OUTPATH,
                  outputname=OUTNAME,
                  excludetypes=EXCLUDETYPES,
                  excludesecret=False,
                  excludesupersecret=False
                  )

from ctypes import LibraryLoader
import sys
from visualisationLoader import VisualisationLoader

library = sys.argv[1]
print(library)

x = visualisationLoader(library)



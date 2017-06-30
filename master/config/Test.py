import buildbot                                                                  
from buildbot.plugins import util, steps                          
                                                                                  
def getTestFactory():                                                      
                                                     
                                                                                 
    f = util.BuildFactory()                                                      
                                                                                  
    # Determine the build directory.                                             
    f.addStep(                                                                   
        buildbot.steps.shell.SetProperty(                                        
             name        = "get_builddir",                                        
             command     = ["pwd"],                                               
             property    = "builddir",                                            
             description = "set build dir",                                       
             workdir     = "."))

    return f

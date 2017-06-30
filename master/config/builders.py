
import LLVMBuilder
import Test
# Plain LLVM builders.
def _get_llvm_builders():
    return [
        {'name': "llvm-x86-linux",
         'workernames': ["llvm-worker"],
         'factory': LLVMBuilder.getLLVMCMakeBuildFactory(
                        install = None,
                        config_name = 'Release',
                        extra_cmake_args = ["-DLLVM_TARGET_ARCH=x86",
                                          "-DLLVM_ENABLE_ASSERTIONS=ON"],
                        env = {'CC': 'clang',
                                'CXX': 'clang++',
                              })
         },

        {'name': "Test",
         'workernames': ["llvm-worker"],
         'factory': Test.getTestFactory()
         }
    ]



def get_builders():
    for b in _get_llvm_builders():
        yield b


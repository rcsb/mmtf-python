try:
    import numpy
    from .decoders import run_length_decode
    from .numpy_decoders import delta_decode
except ImportError:
    from .decoders import run_length_decode,delta_decode
v_base = "0.0.1"
__version__ = v_base+"+dev" if __import__("os").getenv("_YP_HATCH_BUILD_MODE", "release") == "dev" else v_base

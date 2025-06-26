{ pkgs }: {
  deps = [
    pkgs.ffmpeg
    pkgs.libjpeg
    pkgs.zlib
    pkgs.freetype
    pkgs.python3
    pkgs.python3Packages.pillow
    pkgs.python3Packages.setuptools
  ];
}

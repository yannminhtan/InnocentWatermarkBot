{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.python311Packages.pillow
    pkgs.python311Packages.moviepy
    pkgs.python311Packages.numpy
    pkgs.python311Packages.imageio
    pkgs.python311Packages.tqdm
    pkgs.python311Packages.setuptools
    pkgs.python311Packages.pip
    pkgs.ffmpeg_4
  ];
}

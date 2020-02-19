# Hijacking Pop!\_OS
*February 19, 2020*

![](/static/images/pop-debian.png)
The boring but descriptive title: *Configuring and installing the Pop!\_OS
theming and tools on Debian based distributions other then Pop!\_OS.*

I 🖤 the work the system76 team has put into the theming and tooling for
Pop. `system76-power` is super handy and the `pop-gtk` theme is the only theme
I can comfortably daily drive but the lack of customizability of the drive
parition layout and file system types to enable things such as hibernation
or zfs during the install and the unstablity I have been experiencing
whilst using the distro's backported nvidia drivers leaves me in a situation
where I want to love Pop but have to look else where. But why not have both
a different underlying distro and the Pop tooling and theming!

So that's what I did.

Starting out with a fresh Debian Buster install with gnome installed, (I like to
use the package `gnome-core` because it doesn't install any of the gnome
recommended apps which I never use such as `gnome-contacts`)
the first thing I did was add the Pop ppa. Now before you scream
"[Don't break Debian!](https://wiki.debian.org/DontBreakDebian)", as long as
the repo is correctly pinned and we don't try to install anything potentially
system breaking such as the Nvidia drivers, kernel, gnome, etc.
the system will be fine as it will mostly just be harmless configuration files
and some theming.

```
# apt-add-repository ppa:system76/pop
# apt update
```

Now lets make sure no packages are installed from the Pop ppa unless
explicitly installed.

`/etc/apt/preferences.d/pop`

```
Package: *
Pin: release o=LP-PPA-system76-pop
Pin-Priority: 100
```

Now Pop!\_OS is awesome cos all of the distro configuration is handled by
Debian packages which on install configure the system. All of Pop's custom
packages can be found on the [pop-os github](https://github.com/pop-os) but
the most interesting one imo is
[default-settings](https://github.com/pop-os/default-settings). The
`default-settings` package not only contains Pop's gconf settings but it also
depends on the rest of the theming acting as a nice metapackage.

One slight problem with `default-settings` though is that it tries to add
the Pop propriety repo automatically which fails on Debian because `buster`
isn't a valid Ubuntu version code name. Thus I have created a fork which
removes this feature
([github.com/hugglesfox/pop-default-settings](https://github.com/hugglesfox/pop-default-settings))
but that means that it needs to be manually compiled.

```
$ git clone https://github.com/hugglesfox/pop-default-settings
$ cd pop-default-settings
$ debuild -us -uc
$ sudo apt install ../pop-default-settings*.deb
```

Now we have pulled in all the pop theming we just need to do a few more tweaks
to make it perfect such as setting the gtk and gnome shell theme in the
`gnome-tweak-tool`

![](/static/images/pop-debian-theme-tweaks.png)

and whilst in the tweak tool, setting the fonts to the
[recommended fonts](https://github.com/pop-os/fonts#recommendations)

![](/static/images/pop-debian-fonts.png)

That's about it. I have also successfully tried this on a custom Ubuntu install
with ZFS on root (my current set up). Isn't FOSS great!?

Happy hacking

H

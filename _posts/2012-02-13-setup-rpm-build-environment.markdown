---
layout: post
title:  "Setup RPM build environment"
date:   2014-06-02 21:00:00 +0200
categories: system
---
* This will become a table of contents (this text will be scrapped).
{:toc}

# On RedHat based systems

To build a RPM, you need to prepare your system with packages, libraries a specific configuration file and optionally a way to sign created packets. We’re going through all these as quickly as possible.

## Foreword

Building packets doesn’t require you any specific rights - just a plain user account. In fact, it’s really really a good idea to build packets under an unprivileged user as you won’t be able to do any damage on the system itself if you’re doing something wrong.

> [!CAUTION] TL;DR; : don’t use root to build packages ! NEVER !

## Installing prerequisites

In order to be ready to build a package, your system needs to have some packages and libraries installed. We are going to install the most common ones; if your package requires one, just install it. (This should be done as root)

> [!NOTE] Note: We are going to install a lot of packages containing scripts and pieces coming providing help for setuping and maintaining build environments from the sister distribution, Fedora.

```bash
yum install glibc rpmbuild rpmdevtools yum-utils make
yum groupinstall "Fedora Packager" #Contains a bunch of scripts and tools
```

## Creating a GPG key

> [!NOTE] Note: This step is optional, if you don’t want having your packets signed, then just skip this part.

What we are going to do here, is create a GPG private/public key pair in order to sign your packets. The interrest of this is that there is a guarantee for the people that are usually installing your packets that the packet hasn’t been modified, otherwise a GPG error would just pop up. Doing this is pretty straight as it’s just firing one command.

```bash 
gpg --gen-key
=>	gpg (GnuPG) 2.0.14; Copyright (C) 2009 Free Software Foundation, Inc.
	This is free software: you are free to change and redistribute it.
	There is NO WARRANTY, to the extent permitted by law.

	gpg: répertoire `/home/bkraft/.gnupg' créé
	gpg:  nouveau fichier de configuration `/home/bkraft/.gnupg/gpg.conf' créé
	gpg: AVERTISSEMENT: les options de `/home/bkraft/.gnupg/gpg.conf' ne sont pas encore actives cette fois
	gpg: le porte-clés `/home/bkraft/.gnupg/secring.gpg` a été créé
	gpg: le porte-clés `/home/bkraft/.gnupg/pubring.gpg` a été créé
	Sélectionnez le type de clé désiré:
	   (1) RSA and RSA (default) # This is what we are going to pick
	   (2) DSA and Elgamal
	   (3) DSA (signature seule)
	   (4) RSA (signature seule)
	Votre choix ? 1
	les clés RSA peuvent faire entre 1024 et 4096 bits de longueur.
	Quelle taille de clé désirez-vous ? (2048) 4096 # Make it big
	La taille demandée est 4096 bits
	Spécifiez combien de temps cette clé devrait être valide.
	         0 = la clé n'expire pas
	      <n>  = la clé expire dans n jours
	      <n>w = la clé expire dans n semaines
	      <n>m = la clé expire dans n mois
	      <n>y = la clé expire dans n années
	La clé est valide pour ? (0) # Make it never expires ... don't do this.
	La clé n'expire pas du tout
	Est-ce correct ? (o/N) o

	You need a user ID to identify your key; the software constructs the user ID
	from the Real Name, Comment and Email Address in this form:
	    "Heinrich Heine (Der Dichter) <heinrichh@duesseldorf.de>"

	Nom réel: Benjamin KRAFT
	Adresse e-mail: benj@bkraft.fr
	Commentaire: RPM build purposes
	Vous avez sélectionné ce nom d'utilisateur:
	    "Benjamin KRAFT (RPM build purposes) <benj@bkraft.fr>"

	Changer le (N)om, le (C)ommentaire, l'(E)-mail ou (O)K/(Q)uitter ? O
	Vous avez besoin d'une phrase de passe pour protéger votre clé
	secrète.

	can't connect to `/home/bkraft/.gnupg/S.gpg-agent': Aucun fichier ou dossier de ce type
	gpg-agent[21736]: répertoire `/home/bkraft/.gnupg/private-keys-v1.d' créé
	Un grand nombre d'octets aléatoires doit être généré. Vous devriez faire
	autre-chose (taper au clavier, déplacer la souris, utiliser les disques)
	pendant la génération de nombres premiers; cela donne au générateur de
	nombres aléatoires une meilleure chance d'avoir assez d'entropie.
	gpg: /home/bkraft/.gnupg/trustdb.gpg: base de confiance créée
	gpg: clé 7AC6E47B marquée comme ayant une confiance ultime.
	les clés publique et secrète ont été créées et signées.

	gpg: vérifier la base de confiance
	gpg: 3 marginale(s) nécessaires, 1 complète(s) nécessaires, modèle
	de confiance PGP
	gpg: profondeur: 0  valide:   1  signé:   0
	confiance: 0-. 0g. 0n. 0m. 0f. 1u
	pub   4096R/7AC6E47B 2012-02-04
	    Empreinte de la clé = 38E9 4639 75BD 4715 55DD  28E5 178A 4B6C 7AC6 E47B
	uid                  Benjamin KRAFT (RPM build purposes) <benj@bkraft.fr>
	sub   4096R/379A3BD3 2012-02-04
```

## Note regarding entropy

Entropy on a virtual machine like on the one I did this HOWTO was really low and I was stuck with GnuPG waiting for more of it. Here is what I used as a solution to get it finished :

> #notetoself when gpg –gen-key on vm with low entropy (35) install rng-tools and use /dev/urandom as rng device for rngd.
> — Benjamin KRAFT (@b3nj) https://twitter.com/b3nj/status/165715474963902464 (February 4, 2012)

Well, it seems that it really wasn’t the best solution available, as said @digdns responded :

> @b3nj I recommendhaveged https://issihosts.com/haveged/ (see also: https://web.archive.org/web/20201029110552/http://t.co/UFfD0nO7)
> — JP’s DNS cache (@digdns) https://web.archive.org/web/20201029110552/https://twitter.com/digdns/status/165716319021445120 (February 4, 2012)



We’ll use what we did in a further module, but you should already do the two following things :

```bash
# Export your public key to let systems recognize your signature
gpg --export --armor >RPM-GPG-KEY-benjaminkraft
# Import it in your own system
rpm --import /home/bkraft/RPM-GPG-KEY-benjaminkraft
```

## Setting up the environment

Fire up the appropriate command that will create eveything that is necessary for your build environment

```bash
rpmdev-setuptree # Yeah. that's it.
ls -l 
=>	drwxrwxr-x 7 bkraft bkraft 4096  4 févr. 09:07 rpmbuild
ls -l rpmbuild/
total 20
=>	drwxrwxr-x 2 bkraft bkraft 4096  4 févr. 09:07 BUILD
	drwxrwxr-x 2 bkraft bkraft 4096  4 févr. 09:07 RPMS
	drwxrwxr-x 2 bkraft bkraft 4096  4 févr. 09:07 SOURCES
	drwxrwxr-x 2 bkraft bkraft 4096  4 févr. 09:07 SPECS
	drwxrwxr-x 2 bkraft bkraft 4096  4 févr. 09:07 SRPMS
cat .rpmmacros 
=>	%_topdir      %(echo $HOME)/rpmbuild
	%_smp_mflags  -j3
	%__arch_install_post   /usr/lib/rpm/check-rpaths   /usr/lib/rpm/check-buildroot

Now, add the GnuPG related stuff in order to sign your packages :

	%_topdir      %(echo $HOME)/rpmbuild
	%_smp_mflags  -j3
	%__arch_install_post   /usr/lib/rpm/check-rpaths   /usr/lib/rpm/check-buildroot
	%_signature             gpg
	%_gpg_name              Benjamin KRAFT
	%_gpg_path              %(echo $HOME)/.gnupg
```

## Examples

Now that you’re ready, here is some common things that you’ll like to do:

```bash
# Fedora has more recent packets than CentOS, that's a fact.
# Sometimes, I do backport a package from there to here, by downloading
# a package in src.rpm format and just rebuild it.

# This can be done on one single command line to simply build it
rpmbuild --rebuild package.src.rpm

# Or, install the src.rpm (as the building user), modify the spec, and build
rpm -ivh package.src.rpm
vim rpmbuild/SPEC/package.spec
rpmbuild -bb /rpmbuild/SPEC/package.spec

# Add a GnuPG signature on the created packet
rpmsign --addsign package.el6.noarch.rpm

# Check a GnuPG signature
rpmsign --checksig rpmbuild/RPMS/noarch/package.el6.noarch.rpm 
=>	rpmbuild/RPMS/noarch/package.el6.noarch.rpm: rsa sha1 (md5) pgp md5 OK
```
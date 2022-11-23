# lineage-analysis
Repository containing scripts and data for the analysis of the persistence and growth of arbitrary lineage annotations for SARS-CoV-2 over a series of public phylogenies. 

## Usage

You can obtain a historical time series of protobufs by choosing dates and downloading those days' global phylogenies from [here](http://hgdownload.soe.ucsc.edu/goldenPath/wuhCor1/UShER_SARS-CoV-2/). 

You will need [BTE](https://github.com/jmcbroome/BTE) and [matUtils](https://github.com/yatisht/usher) to be available in your environment. You can install them locally from their repositories or through the bioconda channel.

This repository uses github submodules to wrap the automated lineage prototype. When you clone it, you will need to use --recurse-submodules to correctly initialize it.

```
conda create -n timelin -c conda-forge -c bioconda usher bte pandas snakemake
conda activate timelin
git clone --recurse-submodules https://github.com/jmcbroome/lineage-analysis
```

Once your environment is set up and your files are available, run the following:

```
set -e
touch floating_paths.txt
touch floating_samples_clades.txt
for f in *pb.gz ; do 
    export PREFIX=${f%.all.masked.pb.gz} ; 
    python3 strip_annotations.py $PREFIX.all.masked.pb.gz $PREFIX.cleaned.pb ;
    matUtils annotate -T 4 -i $PREFIX.cleaned.pb -P floating_paths.txt -M floating_paths.txt -c floating_samples_clades.txt -o $PREFIX.pb ; 
    gzip $PREFIX.pb ; 
    cd automate-lineages-prototype ;
    snakemake -c1 -s flag_lineages.smk ../$PREFIX.proposed.report.tsv ; 
    cd .. ; 
    matUtils extract -i $PREFIX.proposed.pb -C floating_paths.base.txt ; 
    awk -F'\t' '{{print $1"\t"$3}}' floating_paths.base.txt | tail -n +2 > floating_paths.txt ; 
    python3 extract_sample_clades.py $PREFIX.proposed.pb > floating_samples_clades.txt ; 
done
```

This automatically infers new lineages on each tree in your time series, propagating inferred lineages between trees. Note that the glob order is alphanumeric- if you use the standard tree name formatting (e.g. public-YYYY-MM-DD) then it should be in the correct time order as well.

Once you've generated all your results files, collect some statistics by running the following.

```
for f in *proposed.pb ; do
    matUtils summary -i $f -c ${f%.proposed.pb}.cladestats.txt ;
done
```

```
python3 compile_reports.py
```

Your results will be visible in compiled_report.tsv. There are adjustable parameters for compile_reports.py (use --help).
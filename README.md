# lineage-analysis
Repository containing scripts and data for the analysis of the persistence and growth of arbitrary lineage annotations for SARS-CoV-2 over a series of public phylogenies. 

## Usage

You can obtain a historical time series of protobufs by choosing dates and downloading those days' global phylogenies from [here](http://hgdownload.soe.ucsc.edu/goldenPath/wuhCor1/UShER_SARS-CoV-2/). 

You will need [BTE](https://github.com/jmcbroome/BTE) and [matUtils](https://github.com/yatisht/usher) to be available in your environment. You can install them locally from their repositories or through the bioconda channel.

This repository uses github submodules to wrap the automated lineage prototype. When you clone it, you will need to use --recurse-submodules to correctly initialize it.

```
conda create -n timelin -c conda-forge -c bioconda usher bte 
conda activate timelin
git clone --recurse-submodules https://github.com/jmcbroome/lineage-analysis
```

Once your environment is set up and your files are available, run the following:

```
for f in *pb.gz ; do 
    export PREFIX=${f%.all.masked.pb.gz} ; 
    matUtils annotate -T 4 -i $PREFIX.all.masked.pb.gz -P floating_paths.txt floating_samples_clades.txt -o $PREFIX.pb ; 
    gzip $PREFIX.pb ; 
    cd automate-lineages-prototype ; 
    snakemake -c1 -s flag_lineages.smk ../$PREFIX.proposed.report.tsv ; 
    cd .. ; 
    matUtils extract -i $PREFIX.proposed.pb –clade-paths floating_paths.base.txt ; 
    awk -F'\t' '{{print $1"\t"$3}}' floating_paths.base.txt | tail -n +2 > floating_paths.txt ; 
    python3 extract_samples_clades.py $PREFIX.proposed.pb > floating_samples_clades.txt ; 
done
```

This automatically infers new lineages on each tree in your time series, propagating inferred lineages between trees. It may not be in the correct order with a simple glob, depending on the dates selected and how they translate to bash default sorting.

Once you've generated all your results files, collect some statistics.

```
for f in *proposed.pb ; do
    matUtils summary -i $f -C ${f%.proposed.pb}.cladestats.txt ;
done 
```

Then you can run the included Jupyter notebook to see how these clade statistics and report files are compiled and lineages are evaluated. 
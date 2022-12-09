import pandas as pd
import numpy as np
import glob
import datetime as dt
import argparse

def parse_date(f):
    prefix = f.strip("./").split(".")[0]
    if len(prefix) == 0:
        return np.nan
    date = dt.datetime.strptime("-".join(prefix.split("-")[1:]), "%Y-%m-%d")
    return date

def read_group(gls):
    dfv = []
    for i,f in enumerate(sorted(glob.glob(gls))):
        date = parse_date(f)
        df = pd.read_csv(f,sep='\t')
        df['date'] = date
        df['num'] = i
        dfv.append(df)
    return pd.concat(dfv)

def argparser():
    parser = argparse.ArgumentParser(description="Compile and filter periodic reports and cladestats files to produce a set of high quality lineages for formal designation.")
    parser.add_argument("-i","--input",default='./',help="Path to a directory containing *report.tsv and *cladestats.txt files to compile. Defaults to the current directory")
    parser.add_argument("-g","--growth",default=0,type=float,help="Minimum weekly periodic percentage change in the size of the lineage over the period after its first appearance. Default is 0, meaning lineages that shrink or remain static over any week are filtered.")
    parser.add_argument("-s","--final_size",default=5,type=int,help="Set a minimum absolute gain in lineage size over the time period examined. Default 5")
    parser.add_argument("-e","--escape_change",default=0,type=float,help="Minimum gain of immune escape as estimated by Bloom DMS data. Default is 0 (no change to escape value).")
    parser.add_argument("-p","--persistence",default=0,type=int,help="Minimum number of consecutive trees since designation to include a lineage. Default 0 (new lineages in the final tree can be accepted).")
    parser.add_argument("-o","--output",default="compiled_report.tsv",help="Name the compiled output report tsv.")
    parser.add_argument("-a","--active",action='store_true',help='Include only lineages that were actively growing within the last week examined.')
    return parser.parse_args()

def main():
    args = argparser()
    rdf = read_group(args.input + "*proposed.report.tsv")
    cdf = read_group(args.input + "*cladestats.txt")
    sizes = cdf.set_index(['clade','num']).sort_index().groupby("clade").inclusive_count.max().to_dict()
    dates = cdf.set_index(['clade','num']).sort_index().groupby("clade").date.max().to_dict()
    tchange = cdf.set_index(['clade','num']).sort_index().groupby("clade").exclusive_count.pct_change()
    slopes = tchange.groupby(level=0).min().to_dict()
    tchange = tchange.reset_index()
    recent = set(tchange[(tchange.num == tchange.num.max()) & (tchange.exclusive_count > 0)].clade)
    rdf['final_date'] = rdf.proposed_sublineage.apply(lambda x:dates.get(x,np.nan))
    rdf['final_size'] = rdf.proposed_sublineage.apply(lambda x:sizes.get(x,np.nan))
    rdf['active'] = rdf.proposed_sublineage.isin(recent)
    rdf['growth'] = rdf.proposed_sublineage.apply(lambda x:slopes.get(x,np.nan))
    pd = cdf.clade.value_counts().to_dict()
    rdf['persistence'] = rdf.proposed_sublineage.apply(lambda x:pd.get(x,np.nan))
    rdf['total_growth'] = rdf['final_size'] - rdf['proposed_sublineage_size']
    #exclude proposed sublineages that are in turn descendents of existing proposals.
    final = rdf[(rdf.total_growth >= args.final_size) & (rdf.net_escape_gain >= args.escape_change) & (rdf.growth > args.growth) & (args.persistence <= rdf.persistence) & (rdf.parent.apply(lambda x:"auto." not in x))]
    final.to_csv(args.output,sep='\t',index=False)

if __name__ == "__main__":
    main()
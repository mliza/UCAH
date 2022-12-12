#!/usr/bin/bash 
#SBATCH --job-name=Sym_Inviscid
#SBATCH --account=chanl 
#SBATCH --partition=standard
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=mliza@email.arizona.edu 
#SBATCH --error=job.%J.err 

#SBATCH --nodes=4           ##number of computers  
#SBATCH --ntasks=8          ##numbers of cores per computer  
#SBATCH --mem=30gb          ##ammount of ram per core  
#SBATCH --time=48:00:00

##  Runs SU2  ##
module load openmpi3 
SU2_CFD *.cfg 

## Runs Lemans ##
#mpiexec $HOME/srcCode/lemans-mopar/build/bin/lemans_mopar  

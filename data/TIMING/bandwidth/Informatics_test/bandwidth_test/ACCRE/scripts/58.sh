#!/bin/bash

#echo "Testing"

ssh kimm58@hickory.accre.vanderbilt.edu "dd if=/nfs2/harmonization/BIDS/WRAP/derivatives/sub-wrap0070/ses-baseline/ConnectomeSpecial/tracks_10000000_compressed.tck bs=20M" | dd of=/tmp/karthik.tck bs=20M
#time scp kimm58@hickory.accre.vanderbilt.edu:/nfs2/harmonization/BIDS/WRAP/derivatives/sub-wrap0070/ses-baseline/ConnectomeSpecial/tracks_10000000_compressed.tck /nobackup/p_masi/kimm58/testaccre.tck

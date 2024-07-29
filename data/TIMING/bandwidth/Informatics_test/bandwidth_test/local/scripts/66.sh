#!/bin/bash

ssh kimm58@zeppelin.vuds.vanderbilt.edu "dd if=/home-local/kimm58/informatics/tracks_10000000_compressed.tck bs=20M" | dd of=/nobackup/p_masi/kimm58/projects/Informatics_test/bandwidth_test/AWS/track.tck bs=20M

#!/bin/bash

ssh -i ~/Kim_Test.pem ubuntu@44.222.225.166 "dd if=~/tracks_10000000_compressed.tck bs=20M" | dd of=/nobackup/p_masi/kimm58/projects/Informatics_test/bandwidth_test/AWS/track.tck bs=20M

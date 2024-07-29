import subprocess

def transfer_speed_test(src, dest):
    """
    Transfer speed test. Run this from landman01
    """
    
    cmd_AWS = "dd if=tracks_10000000_compressed.tck bs=32K | ssh -i ~/Kim_Test.pem ubuntu@44.222.225.166 \"dd of=/tmp/testfile bs=1M oflag=dsync\""
    cmd_local = "dd if=tracks_10000000_compressed.tck bs=32K | ssh kimm58@zeppelin.vuds.vanderbilt.edu \"dd of=/tmp/testfile bs=1M oflag=dsync\""
    cmd_accre = "dd if=tracks_10000000_compressed.tck bs=32K | ssh kimm58@cn1321 \"dd of=/tmp/testfile bs=1M oflag=dsync\""
        #maybe do an accre script instead of sshing in

    # for the job node, replace kimm58@hickory... with kimm58@cnXXXX
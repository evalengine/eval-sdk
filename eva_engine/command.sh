#! /bin/bash

chr query engine_count --network=mainnet --blockchain=eva_engine
chr query tweet_scores_count --network=mainnet --blockchain=eva_engine

chr query get_tweet_scores_by_user_address --network=mainnet --blockchain=eva_engine 'user_address=x"02EF9E21262155811C9EB46AB795E104C9D464FCF7E8554F14C019C0488F0D2E1D"' 'pointer=0' 'n_scores=100' 'end_time=1836485728266' 'start_time=0'

# Update
chr deployment update --settings chromia.yml --network mainnet --blockchain eva_engine 
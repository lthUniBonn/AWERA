import os
from AWERA import config, ChainAWERA
import time
from AWERA.utils.convenience_utils import write_timing_info
since = time.time()

training_settings = []
prediction_settings = []

# Test run on 5 special locations
for i in range(5):
    for j in range(5):
        settings = {
            'Processing': {'n_cores': 10},
            'Data': {
                'n_locs': 1,
                'location_type': 'europe_ref_{}'.format(i)},
            'Clustering': {
                'training': {
                    'n_locs': 1,
                    'location_type': 'europe_ref_{}'.format(j)
                    }
                },
            }
        if i == 0:
            training_settings.append(settings)
        prediction_settings.append(settings)

    settings = {
        'Processing': {'n_cores': 10},
        'Data': {'n_locs': 1,
                 'location_type': 'europe_ref_{}'.format(i)},
        'Clustering': {
            'n_clusters': 8,
            'training': {
                'n_locs': 5,
                'location_type': 'europe_ref'
                }
            },
        }
    if i == 0:
        training_settings.append(settings)
    prediction_settings.append(settings)

    # multiple locations
    settings = {
        'Processing': {'n_cores': 10},
        'Data': {'n_locs': 1,
                 'location_type': 'europe_ref_{}'.format(i)},
        'Clustering': {
            'training': {
                'n_locs': 50,
                'location_type': 'europe'
                }
            },
        }

    if i == 0:
        training_settings.append(settings)
    prediction_settings.append(settings)

    settings = {
        'Processing': {'n_cores': 10},
        'Data': {'n_locs': 1,
                 'location_type': 'europe_ref_{}'.format(i)},
        'Clustering': {
            'training': {
                'n_locs': 200,
                'location_type': 'europe'
                }
            },
        }
    if i == 0:
        training_settings.append(settings)
    prediction_settings.append(settings)

    # Multiple locations plus 5 special locs
    settings = {
        'Processing': {'n_cores': 10},
        'Data': {'n_locs': 1,
                 'location_type': 'europe_ref_{}'.format(i)},
        'Clustering': {
            'training': {
                'n_locs': 55,
                'location_type': 'europe_incl_ref'
                }
            },
        }
    if i == 0:
        training_settings.append(settings)
    prediction_settings.append(settings)

    settings = {
        'Processing': {'n_cores': 10},
        'Data': {'n_locs': 1,
                 'location_type': 'europe_ref_{}'.format(i)},
        'Clustering': {
            'training': {
                'n_locs': 205,
                'location_type': 'europe_incl_ref'
                }
            },
        }
    if i == 0:
        training_settings.append(settings)
    prediction_settings.append(settings)

# very many locations
settings = {
    'Processing': {'n_cores': 23},
    'Data': {'n_locs': 1,
             'location_type': 'europe_ref_1'},
    'Clustering': {
        'training': {
            'n_locs': 5000,
            'location_type': 'europe'
            }
        },
    }
training_settings.append(settings)
# TODO include prediction
settings = {
    'Processing': {'n_cores': 50},
    'Data': {'n_locs': 1,
             'location_type': 'europe_ref_1'},
    'Clustering': {
        'training': {
            'n_locs': 1000,
            'location_type': 'europe'
            }
        },
    }
training_settings.append(settings)
settings = {
    'Processing': {'n_cores': 50},
    'Data': {'n_locs': 1,
             'location_type': 'europe_ref_1'},
    'Clustering': {
        'training': {
            'n_locs': 5005,
            'location_type': 'europe_incl_ref'
            }
        },
    }
training_settings.append(settings)

settings = {
    'Processing': {'n_cores': 23},
    'Data': {'n_locs': 1,
             'location_type': 'europe_ref_1'},
    'Clustering': {
        'training': {
            'n_locs': 1005,
            'location_type': 'europe_incl_ref'
            }
        },
    }
training_settings.append(settings)

# TODO make clear how each module runs with the inout of the previous
# power_model.load() .generate() how is the object made/passed


if __name__ == '__main__':
    # read config from jobnumber
    # 8 small jobs
    # 4 big jobs
    # settings_id = int(os.environ['SETTINGS_ID'])

    # test_final_setup_settings = training_settings[10:12]  # 5000, 1000
    # settings = training_settings[settings_id]
    import os
    if not os.path.exists('tmp'):
        os.makedirs('tmp')
    # read config from jobnumber
    settings_id = int(os.environ['SETTINGS_ID'])

    n_locs_settings = [200, 500, 1000, 5000]
    n_locs = n_locs_settings[settings_id]
    # settings = training_settings[settings_id]
    settings = {
        'Data': {'n_locs': 5000,
                 'location_type': 'europe_ref'},
        'Clustering': {
            'training': {
                'n_locs': n_locs,
                'location_type': 'europe'
                }
            },
        }

    settings['General'] = {'use_memmap': False}  # True}
    settings['Processing'] = {'n_cores': 15}  # 30}  # 50}
    print(settings)
    # Update settings to config
    config.update(settings)

    # Initialise AWERA chain with chosen config
    awera = ChainAWERA(config)

    # Code Profiling
    # TODO include in config -> optional
    # imports at top level / optional
    import cProfile, pstats
    profiler = cProfile.Profile()
    profiler.enable()

    # Run full clustering, production, aep estimation
    # depending on flags set in config
    # TODO include all important flags here to update conveniently

    # TODO check if clustering etc has to be done?

    working_title = 'predict_labels'  # 'run_clustering'  #'run_production'  #  'run_production' # 'file'
    prod_settings = {
       # 'Processing': {'n_cores': 57},
        'Clustering': {'n_clusters': 80}}
    awera.config.update(prod_settings)
    awera.predict_labels()
    print('80 clusters done.')
    write_timing_info('{} AWERA run finished.'.format(working_title),
                      time.time() - since)
    prod_settings = {
        #'Processing': {'n_cores': 57},
        'Clustering': {'n_clusters': 8}}
    awera.config.update(prod_settings)
    awera.predict_labels()
    # profiles, data = awera.train_profiles(return_data=True)
    # limit_estimates = awera.estimate_wind_speed_operational_limits()
    # pcs, limit_refined = awera.make_power_curves(limit_estimates=limit_estimates)
    # awera.compare_kpis(pcs)
    print('8 clusters done.')
    print('------------------------------ Time:')
    write_timing_info('{} AWERA run finished.'.format(working_title),
                      time.time() - since)
    prod_settings = {
        #'Processing': {'n_cores': 57},
        'Clustering': {'n_clusters': 16}}
    awera.config.update(prod_settings)
    awera.predict_labels()
    # profiles = awera.train_profiles(data=data)
    # limit_estimates = awera.estimate_wind_speed_operational_limits()
    # pcs, limit_refined = awera.make_power_curves(limit_estimates=limit_estimates)
    # awera.compare_kpis(pcs)
    print('16 clusters done.')
    print('------------------------------ Time:')
    write_timing_info('{} AWERA run finished.'.format(working_title),
                      time.time() - since)

    # profiles = awera.train_profiles(data=data)
    # limit_estimates = awera.estimate_wind_speed_operational_limits()
    # pcs, limit_refined = awera.make_power_curves(limit_estimates=limit_estimates)
    # awera.compare_kpis(pcs)


    print('Done.')
    print('------------------------------ Config:')
    print(awera.config)
    print('------------------------------ Time:')
    write_timing_info('{} AWERA run finished.'.format(working_title),
                      time.time() - since)
    profiler.disable()
    # # Write profiler output
    file_name = awera.config.IO.plot_output.replace('.pdf', '.profile')

    with open(file_name.format(title='run_profile'), 'w') as f:
        stats = pstats.Stats(profiler, stream=f)
        stats.strip_dirs()
        stats.sort_stats('cumtime')
        stats.print_stats('py:', .1)
    print('Profile output written to: ',
          file_name.format(title=working_title))


    #plt.show()




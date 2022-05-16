import os
from AWERA import config, ChainAWERA
import time
from AWERA.utils.convenience_utils import write_timing_info
since = time.time()


if __name__ == '__main__':
    # read config from jobnumber
    # 8 small jobs
    # 4 big jobs
    settings_id = int(os.environ['SETTINGS_ID'])

    n_clusters_settings = [8, 24]  # 16, 80]
    n_clusters = n_clusters_settings[settings_id]

    # n_locs = 1 # [200, 500, 1000, 5000]
    n_l = 1  # n_locs[settings_id]
    scan_tag = 'fix_vw_'  # more_
    settings = {
        'Data': {'n_locs': 1,
                 'location_type': 'Maasvlakte_2'},
        'Clustering': {
            'n_clusters': n_clusters,
            'training': {
                'n_locs': n_l,
                'location_type': 'Maasvlakte_2'
                }
            },
        'Processing': {'n_cores': n_clusters},
        'General': {'ref_height': 100},
        # 'Power':{ 'bounds': bounds},
        'IO': {
            'result_dir': "/cephfs/user/s6lathim/AWERA_results_Rotterdam/",
            'format': {
                'plot_output':
                    scan_tag + config.IO.format.plot_output,
                'power_curve':
                    scan_tag + config.IO.format.power_curve,
                'cut_wind_speeds':
                    scan_tag + config.IO.format.cut_wind_speeds,
                'refined_cut_wind_speeds':
                    scan_tag + config.IO.format.refined_cut_wind_speeds,
                # Only Power Production - no chain plot output for now
                'plot_output_data':
                    scan_tag + config.IO.format.plot_output_data,
                'training_plot_output':
                    scan_tag + config.IO.format.training_plot_output,
                'freq_distr':
                    scan_tag + config.IO.format.freq_distr,
                    }
                }
        }
    # settings['General'] = {'use_memmap': True}
    # settings[
    print(settings)
    # Update settings to config
    config.update(settings)

    print(config)

    # Initialise AWERA chain with chosen config
    awera = ChainAWERA(config)

    # Code Profiling
    # TODO include in config -> optional
    # imports at top level / optional

    # import cProfile, pstats
    # profiler = cProfile.Profile()
    # profiler.enable()

    # Run full clustering, production, aep estimation
    # depending on flags set in config
    # TODO include all important flags here to update conveniently

    # TODO check if clustering etc has to be done?

    working_title = 'run_production'  #  'run_production' #'predict_labels' #  'file'
    # awera.run_clustering()
    # awera.plot_cluster_shapes()
    limit_estimates = awera.estimate_wind_speed_operational_limits()
    pcs, limit_refined = awera.make_power_curves(limit_estimates=limit_estimates)
    awera.compare_kpis(pcs)

    print(awera.read_limits(refined=True))
    print(awera.read_profiles())
    awera.plot_power_curves(plot_full_electrical=True)
    awera.plot_power_curves(speed_at_op_height=True,
                            plot_full_electrical=True)
    awera.get_frequency()
    awera.plot_cluster_frequency()
    awera.aep()

    print('Done.')
    print('------------------------------ Config:')
    print(awera.config)
    print('------------------------------ Time:')
    write_timing_info('{} AWERA run finished.'.format(working_title),
                      time.time() - since)
    # profiler.disable()
    # # # Write profiler output
    # file_name = awera.config.IO.plot_output.replace('.pdf', '.profile')

    # with open(file_name.format(title='run_profile'), 'w') as f:
    #     stats = pstats.Stats(profiler, stream=f)
    #     stats.strip_dirs()
    #     stats.sort_stats('cumtime')
    #     stats.print_stats('py:', .1)
    # print('Profile output written to: ',
    #       file_name.format(title=working_title))


    #plt.show()




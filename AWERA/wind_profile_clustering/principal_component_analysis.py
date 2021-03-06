from sklearn.decomposition import PCA
from itertools import accumulate
import numpy as np

import matplotlib as mpl
if __name__ != '__main__':
    import matplotlib.pyplot as plt

from .read_requested_data import get_wind_data

from matplotlib.colors import ListedColormap, LogNorm

xlim_pc12 = [-1.6, 1.6]  # [-1.1, 1.1]
ylim_pc12 = [-1.6, 1.6]  # [-1.1, 1.1]
x_lim_profiles = [-0.8, 1.25]


def plot_mean_and_pc_profiles(config,
                              altitudes,
                              var,
                              get_profile):
    plot_n_pcs = 2
    n_cols = 3
    n_rows = plot_n_pcs
    shape_map = (n_rows, n_cols)

    x_label = r"$\tilde{v}$ [-]"
    figsize = (8.4, 6)

    fig, ax = plt.subplots(shape_map[0],
                           shape_map[1],
                           sharey=True,
                           figsize=figsize)
    wspace = 0.1
    layout = {'top': 0.9, 'bottom': 0.085, 'left': 0.38,
              'right': 0.985, 'hspace': 0.23}
    plt.subplots_adjust(**layout, wspace=wspace)

    # Add plot window for mean wind profile to
    # existing plot windows and plot it.
    w, h, y0, x0 = ax[0, 0]._position.width, ax[0, 0]._position.height, \
        ax[0, 0]._position.y0, ax[0, 0]._position.x0
    ax_mean = fig.add_axes([x0-w*(1.5), y0, w, h])

    prl, prp = get_profile()
    ax_mean.plot(prl, altitudes, label="Parallel", color='#ff7f0e')
    ax_mean.plot(prp, altitudes, label="Perpendicular", color='#1f77b4')
    ax_mean.plot((prl**2 + prp**2)**.5, altitudes, '--', label='Magnitude',
                 ms=3, color='#2ca02c')
    ax_mean.set_title("Mean")
    ax_mean.grid(True)
    ax_mean.set_ylabel("Height [m]")
    ax_mean.set_xlim(x_lim_profiles)
    ax_mean.set_xlabel(x_label)
    ax_mean.legend(bbox_to_anchor=(1., 1.16, 3, 0.2), loc="lower left",
                   mode="expand", borderaxespad=0, ncol=4)

    # Add plot window for hodograph to existing plot windows and plot it.
    y0 = ax[1, 0]._position.y0 + .05
    ax_tv = fig.add_axes([x0-w*(1.5), y0, w, h])
    ax_tv.plot(prl, prp, color='#7f7f7f')
    ax_tv.plot([0, prl[0]], [0, prp[0]], ':', color='#7f7f7f')
    ax_tv.grid(True)
    ax_tv.axes.set_aspect('equal')
    ax_tv.set_xlabel(r"$\tilde{v}_{\parallel}$ [-]")
    ax_tv.set_ylabel(r"$\tilde{v}_{\bot}$ [-]")
    ax_tv.set_xlim(x_lim_profiles)
    ax_tv.set_ylim([-.3, .3])

    # Plot PCs and PC multiplicands superimposed on the mean.
    marker_counter = 0
    for i_pc in range(plot_n_pcs):  # For every PC/row in the plot.
        ax[i_pc, 0].set_ylabel("Height [m]")
        std = var[i_pc]**.5
        factors = iter([-1*std, 1*std])

        for i_col in range(n_cols):
            # Get profile data.
            if i_col == 0:  # Column showing solely the PCs
                prl, prp = get_profile(i_pc, 1, True)
                ax[i_pc, i_col].set_xlim(xlim_pc12)
                ax[i_pc, i_col].set_title("PC{}".format(i_pc+1))
            else:  # Columns showing PC multiplicands superimposed on the mean.
                factor = next(factors)
                prl, prp = get_profile(i_pc, factor, False)
                ax[i_pc, i_col].set_xlim(x_lim_profiles)
                ax[i_pc, i_col].set_title(r"Mean{:+.2f}$\cdot$PC{}".format(
                    factor, i_pc+1))

            # Plot profiles.
            ax[i_pc, i_col].plot(prl, altitudes, label="Parallel",
                                 color='#ff7f0e')
            ax[i_pc, i_col].plot(prp, altitudes, label="Perpendicular",
                                 color='#1f77b4')

            if i_col > 0:
                # For columns other than PC column, also plot magnitude line.
                mag = np.sqrt((prl**2 + prp**2))
                ax[i_pc, i_col].plot(mag, altitudes, '--', label='Magnitude',
                                     ms=3, color='#2ca02c')

                marker_counter += 1
                ax[i_pc, i_col].plot(0.1, 0.1, 's', mfc="white", alpha=1,
                                     ms=12, mec='k',
                                     transform=ax[i_pc, i_col].transAxes)
                ax[i_pc, i_col].plot(0.1, 0.1,
                                     marker='${}$'.format(marker_counter),
                                     alpha=1, ms=7, mec='k',
                                     transform=ax[i_pc, i_col].transAxes)
            ax[i_pc, i_col].grid(True)

    # Add labels on x-axes.
    for i_col in range(shape_map[1]):
        if i_col == 0:
            ax[-1, i_col].set_xlabel("Coefficient of PC [-]")
        else:
            ax[-1, i_col].set_xlabel(x_label)
    if not config.Plotting.plots_interactive:
        plt.savefig(config.IO.training_plot_output
                    .format(title='pc_mean_and_pc_profiles'))


def plot_pc_profiles(config, altitudes, get_profile):
    x_label = r"$\tilde{v}$ [-]"

    # Plot PCs
    for i_pc in range(config.Clustering.n_pcs):
        # Plot profiles.
        cm = 1/2.54
        fig = plt.figure(figsize=(15*cm, 20*cm))
        ax = fig.add_subplot(111)

        ax.set_ylabel("Height [m]")
        ax.set_xlim(xlim_pc12)
        ax.set_title("PC{}".format(i_pc+1))
        ax.grid(True)
        ax.set_xlabel(x_label)

        prl, prp = get_profile(i_pc, 1, True)
        ax.plot(prl, altitudes, label="Parallel", color='#ff7f0e')
        ax.plot(prp, altitudes, label="Perpendicular", color='#1f77b4')

        mag = np.sqrt((prl**2 + prp**2))
        ax.plot(mag, altitudes, '--', label='Magnitude', ms=3, color='#2ca02c')

        if not config.Plotting.plots_interactive:
            plt.savefig(config.IO.training_plot_output
                        .format(title=('pc_profile_{}'.format(i_pc+1))))

    fig = plt.figure(figsize=(15*cm, 20*cm))
    ax = fig.add_subplot(111)

    ax.set_ylabel("Height [m]")
    ax.set_xlim(xlim_pc12)
    ax.set_title("Sample Mean")
    ax.grid(True)
    ax.set_xlabel(x_label)

    prl, prp = get_profile()
    ax.plot(prl, altitudes, label="Parallel", color='#ff7f0e')
    ax.plot(prp, altitudes, label="Perpendicular", color='#1f77b4')

    mag = np.sqrt((prl**2 + prp**2))
    ax.plot(mag, altitudes, '--', label='Magnitude', ms=3, color='#2ca02c')

    if not config.Plotting.plots_interactive:
        plt.savefig(config.IO.plot_output
                .format(title=('pc_profile_mean')))


def plot_frequency_projection(config, data_pc):
    fig, ax = plt.subplots(1, 1, figsize=(5, 2.5))
    plt.subplots_adjust(top=0.975, bottom=0.178, left=0.15, right=0.94)

    # Create color map that yields more contrast for
    # lower values than the baseline colormap.
    # cmap_baseline = plt.get_cmap('bone_r')
    # frac = .7
    # clrs_low_values = cmap_baseline(np.linspace(0., .5, int(256*frac)))
    # clrs_low_values[0, :] = 0.
    # clrs_high_values = cmap_baseline(np.linspace(.5, 1., int(256*(1-frac))))
    # cmap = ListedColormap(np.vstack((clrs_low_values, clrs_high_values)))
    # TODO reimplement Logscale...
    cmap = plt.get_cmap('bone_r')
    # cmap.set_bad('white', 1.)
    n_bins = 120
    vmax = 5000
    # norm = LogNorm()  # vmin=1, vmax=vmax)
    h, _, _, im = plt.hist2d(data_pc[:, 0], data_pc[:, 1], bins=n_bins,
                             cmap=cmap)  # norm=norm)  # cmin=1)
    print(np.sum(h == 0), np.sum(np.isnan(h)))
    h_max = np.nanmax(h)
    print("Max occurences in hist2d bin:", str(h_max))
    if vmax is not None and h_max > vmax:
        print("Higher density occurring than anticipated. Replotting...")
        # norm = LogNorm(vmin=1, vmax=h_max)
        # h, _, _, im = plt.hist2d(data_pc[:, 0], data_pc[:, 1], bins=n_bins,
        #                          cmap=cmap, norm=norm, cmin=1)

    #cbar_ax, _ = mpl.colorbar.make_axes(ax)
    # TODO fix log norm colorbar error because of empty bins?
    #np.seterr(all='raise', under='ignore')
    cbar = plt.colorbar(im)
    #np.seterr(all='raise')
    #cbar = mpl.colorbar.ColorbarBase(cbar_ax, norm=norm, cmap=cmap)
    #cbar.set_label("Occurrences [-]")

    plt.xlim(xlim_pc12)
    plt.ylim(ylim_pc12)
    plt.grid()
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    if not config.Plotting.plots_interactive:
        plt.savefig(config.IO.plot_output
                    .format(title='pc_frequency_projection'))



def analyse_pc(config, wind_data, loc_info="", pipeline=None, n_pcs=5):
    # TODO config plot output, remove loc info
    altitudes = wind_data['altitude']
    normalized_data = wind_data['training_data']
    # Perform principal component analyis.
    if pipeline is None:
        n_features = n_pcs
        pca = PCA(n_components=n_features)
        pipeline = pca

    # print("{} features reduced to {} components.".format(
    #     n_features, n_components))
    data_pc = pipeline.fit_transform(normalized_data)
    print("{:.1f}% of variance retained ".format(
        np.sum(pipeline.explained_variance_ratio_[:2])*100)
        + "using first two principal components.")
    cum_var_exp = list(accumulate(pipeline.explained_variance_ratio_*100))
    print("Cumulative variance retained: " + ", ".join(["{:.2f}".format(var)
                                                        for var in cum_var_exp]
                                                       ))
    var = pipeline.explained_variance_

    # Plot results.
    # TODO same here config, loc info
    plot_frequency_projection(config, data_pc)
    markers_pc1, markers_pc2 = [-var[0]**.5, var[0]**.5, 0, 0], \
        [0, 0, -var[1]**.5, var[1]**.5]
        # TODO what is this?
    plt.plot(markers_pc1, markers_pc2, 's', mfc="white",
             alpha=1, ms=12, mec='k')
    for i, (pc1, pc2) in enumerate(zip(markers_pc1, markers_pc2)):
        plt.plot(pc1, pc2, marker='${}$'.format(i+1), alpha=1, ms=7, mec='k')
    if not config.Plotting.plots_interactive:
        plt.savefig(config.IO.plot_output
                    .format(title='pc_frequency_projection_markers'))

    def get_pc_profile(i_pc=-1, multiplier=1., plot_pc=False):
        # Determine profile data by transforming data
        # in PC to original coordinate system.
        if i_pc == -1:
            mean_profile = pipeline.inverse_transform(np.zeros(n_features))
            profile = mean_profile
        else:
            profile_cmp = np.zeros(n_features)
            profile_cmp[i_pc] = multiplier
            profile = pipeline.inverse_transform(profile_cmp)
            if plot_pc:
                mean_profile = pipeline.inverse_transform(np.zeros(n_features))
                profile -= mean_profile
        prl = profile[:len(altitudes)]
        prp = profile[len(altitudes):]
        return prl, prp

    plot_mean_and_pc_profiles(config,
                              altitudes,
                              var,
                              get_pc_profile)


def plot_sample_profile_pc_sum(config,
                               sample_profile,
                               altitudes,
                               get_profile,
                               plot_cluster_profile=None,
                               loc_tag=''):
    plot_n_pcs = 2
    n_cols = 3
    n_rows = plot_n_pcs
    shape_map = (n_rows, n_cols)

    x_label = r"$\tilde{v}$ [-]"
    figsize = (8.4, 6)

    fig, ax = plt.subplots(shape_map[0],
                           shape_map[1],
                           sharey=True,
                           figsize=figsize)
    wspace = 0.1
    layout = {'top': 0.9, 'bottom': 0.085, 'left': 0.38,
              'right': 0.985, 'hspace': 0.23}
    plt.subplots_adjust(**layout, wspace=wspace)

    # Add plot window for orginal profile
    w, h, y0, x0 = ax[0, 0]._position.width, ax[0, 0]._position.height,\
        ax[0, 0]._position.y0, ax[0, 0]._position.x0
    ax_mean = fig.add_axes([x0-w*(1.5), y0, w, h])

    prl, prp = sample_profile[:len(altitudes)], sample_profile[len(altitudes):]
    ax_mean.plot(prl, altitudes, label="Parallel", color='#ff7f0e', zorder=2)
    ax_mean.plot(prp, altitudes, label="Perpendicular", color='#1f77b4',
                 zorder=2)
    ax_mean.plot((prl**2 + prp**2)**.5, altitudes, '--', label='Magnitude',
                 ms=3, color='#2ca02c', zorder=2)
    if plot_cluster_profile is not None:
        prl, prp, i_cluster = plot_cluster_profile
        ax_mean.plot(prl, altitudes, label="", color='#ff7f0e',
                     linestyle='dashdot', alpha=0.5, zorder=1)
        ax_mean.plot(prp, altitudes, label="", color='#1f77b4',
                     linestyle='dashdot', alpha=0.5, zorder=1)
        ax_mean.plot((prl**2 + prp**2)**.5, altitudes, label='',
                     ms=3, color='#2ca02c', linestyle='dashdot', alpha=0.5,
                     zorder=1)
        txt = '${}$'.format(int(i_cluster+1))
        cmap = plt.get_cmap("gist_ncar")
        i = i_cluster
        if config.Clustering.n_clusters > 25:
            if i % 2 == 1:
                if config.Clustering.n_clusters % 2 == 1:
                    shift = -1
                else:
                    shift = 0
                i_c = -i + shift
            else:
                i_c = i
        else:
            i_c = i
        clrs = cmap(np.linspace(0.03, 0.97, config.Clustering.n_clusters))
        ax_mean.plot(0.1, 0.1, 'o', mfc=clrs[i_c],
                     ms=14, mec='k', alpha=0.5, zorder=2,
                     transform=ax_mean.transAxes)  # "white"
        ax_mean.plot(0.1, 0.1, marker=txt, ms=7, mec='k',
                     transform=ax_mean.transAxes, alpha=0.5, zorder=2)
    ax_mean.set_title("Sample Profile")
    ax_mean.grid(True)
    ax_mean.set_ylabel("Height [m]")
    ax_mean.set_xlim(x_lim_profiles)
    ax_mean.set_xlabel(x_label)
    ax_mean.legend(bbox_to_anchor=(1., 1.16, 3, 0.2), loc="lower left",
                   mode="expand",
                   borderaxespad=0, ncol=4)

    # Plot PCs and PC multiplicands superimposed on the mean.
    marker_counter = 0
    i_plot_step = 0
    for i_pc in range(plot_n_pcs):  # For every PC/row in the plot.
        ax[i_pc, 0].set_ylabel("Height [m]")
        for i_col in range(n_cols):
            # Get profile data.
            if i_col == 0 and i_pc == 0:
                # plot mean profile
                prl, prp = get_profile()
                ax[i_pc, i_col].set_xlim(x_lim_profiles)
                ax[i_pc, i_col].set_title("Mean")
            else:  # Plots showing PC contributions superimposed on the mean.
                i_plot_step += 1
                prl, prp = get_profile(-2, sum_step=i_plot_step)
                ax[i_pc, i_col].set_xlim(x_lim_profiles)
                if i_plot_step > 2:
                    ax[i_pc, i_col].set_title("Mean+PC1$\dots$PC{}".format(
                        i_plot_step))
                elif i_plot_step == 2:
                    ax[i_pc, i_col].set_title("Mean+PC1+PC2")
                else:
                    ax[i_pc, i_col].set_title("Mean+PC{}".format(i_plot_step))

            # Plot profiles.
            # Plot magnitude
            ax[i_pc, i_col].plot(prl, altitudes, label="Parallel",
                                 color='#ff7f0e')
            ax[i_pc, i_col].plot(prp, altitudes, label="Perpendicular",
                                 color='#1f77b4')

            mag = np.sqrt((prl**2 + prp**2))
            ax[i_pc, i_col].plot(mag, altitudes, '--', label='Magnitude', ms=3,
                                 color='#2ca02c')

            marker_counter += 1
            ax[i_pc, i_col].plot(0.1, 0.1, 's', mfc="white", alpha=1, ms=12,
                                 mec='k', transform=ax[i_pc, i_col].transAxes)
            ax[i_pc, i_col].plot(0.1, 0.1,
                                 marker='${}$'.format(marker_counter),
                                 alpha=1, ms=7,
                                 mec='k', transform=ax[i_pc, i_col].transAxes)
            ax[i_pc, i_col].grid(True)
    if plot_cluster_profile is not None:
        prl, prp, i_cluster = plot_cluster_profile
        ax[i_pc, i_col].plot(prl, altitudes, label="Parallel", color='#ff7f0e',
                             linestyle='dashdot', alpha=0.5, zorder=1)
        ax[i_pc, i_col].plot(prp, altitudes, label="Perpendicular",
                             color='#1f77b4', linestyle='dashdot',
                             alpha=0.5, zorder=1)
        ax[i_pc, i_col].plot((prl**2 + prp**2)**.5, altitudes,
                             label='Magnitude', ms=3, color='#2ca02c',
                             linestyle='dashdot', alpha=0.5, zorder=1)

    # Add labels on x-axes.
    for i_col in range(shape_map[1]):
        ax[-1, i_col].set_xlabel(x_label)
    if not config.Plotting.plots_interactive:
        if plot_cluster_profile is None:
            plt.savefig(config.IO.plot_output
                        .format(title='pc_sample_mean_and_pc_contrib'))
        else:
            plt.savefig(config.IO.plot_output
                        .format(
                            title='pc_sample_mean_and_pc_contrib_vs_cluster{}'
                            .format(loc_tag)))


def sample_profile_pc_sum(config,
                          wind_data, n_pcs=5, i_sample=0,
                          pca_pipeline=None,
                          plot_cluster_profile=None,
                          loc_tag=''):
    altitudes = wind_data['altitude']
    normalized_data = wind_data['training_data']
    # Perform principal component analyis.
    n_features = n_pcs
    if pca_pipeline is None:
        pca = PCA(n_components=n_features)
        pipeline = pca
        # print("{} features reduced to {} components.".format(
        #     n_features, n_components))
        data_pc = pipeline.fit_transform(normalized_data)
    else:
        pipeline = pca_pipeline
        data_pc = pipeline.transform(normalized_data)

    # Plot results.
    def get_pc_profile(i_pc=-1, multiplier=1., plot_pc=False, sum_step=1):
        # Determine profile data by transforming data in PC
        # to original coordinate system.
        if i_pc == -1:
            mean_profile = pipeline.inverse_transform(np.zeros(n_features))
            profile = mean_profile
        elif i_pc == -2:
            # sequential sum of pca profile
            sample_pca_profile_factors = data_pc[i_sample, :]
            profile_cmp = np.zeros(n_features)
            for i in range(sum_step):
                profile_cmp[i] = sample_pca_profile_factors[i]
            profile = pipeline.inverse_transform(profile_cmp)
        else:
            profile_cmp = np.zeros(n_features)
            profile_cmp[i_pc] = multiplier
            profile = pipeline.inverse_transform(profile_cmp)
            if plot_pc:
                mean_profile = pipeline.inverse_transform(np.zeros(n_features))
                profile -= mean_profile
        prl = profile[:len(altitudes)]
        prp = profile[len(altitudes):]
        return prl, prp

    plot_pc_profiles(config, altitudes, get_pc_profile)
    plot_sample_profile_pc_sum(config,
                               normalized_data[i_sample, :],
                               altitudes,
                               get_pc_profile,
                               plot_cluster_profile=plot_cluster_profile,
                               loc_tag=loc_tag)


if __name__ == '__main__':
    from ..config import Config
    config = Config()

    if not config.Plotting.plots_interactive:
        mpl.use('Pdf')
    import matplotlib.pyplot as plt

    import time
    since = time.time()

    wind_data = get_wind_data(config)

    time_elapsed = time.time() - since
    print('Input read - Time lapsed: ', '\t{:.0f}m {:.0f}s'.format(
        time_elapsed // 60, time_elapsed % 60))

    from .preprocess_data import preprocess_data
    wind_data = preprocess_data(config, wind_data)

    time_elapsed = time.time() - since
    print('Preprocessing done - Time lapsed: ', '\t{:.0f}m {:.0f}s'.format(
        time_elapsed // 60, time_elapsed % 60))

    # Run principal component analysis
    analyse_pc(config, wind_data,
               loc_info=config.Data.data_info,
               n_pcs=config.Clustering.n_pcs)
    sample_profile_pc_sum(config, wind_data, i_sample=100,
                          loc_info=config.Data.data_info,
                          n_pcs=config.Clustering.n_pcs)

    time_elapsed = time.time() - since
    print('PCA analysis done - Time lapsed: ', '\t{:.0f}m {:.0f}s'.format(
        time_elapsed // 60, time_elapsed % 60))

    if config.Plotting.plots_interactive:
        plt.show()

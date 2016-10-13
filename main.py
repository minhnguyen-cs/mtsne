__author__ = 'minh'

import numpy as np

import preprocess
import eros
import distance_metric
import pca
import mtsne
import graph_plot

#label for visualization
label_map = {0 : 'Before chemo date #1', 1 :'Chemo date #1', 2 : 'Between chemo dates #1 and #2', 3 : 'Chemo date #2', 4 : 'After chemo date #2'}
label_map_eeg = {0 : 'Control', 1 : 'Alcoholic'}

#run different dataset
RUN_ATOMHP = True
PREPROCESS_ATOMHP = './Preprocess/Your-dataset'

#discard noisy data
DISCARD_ZEROS = False

if __name__ == "__main__":
    if RUN_ATOMHP:
        """
        +   data: array of multiple multivariate time series (MTS)
                  Each MTS is from one subject, has 5 variables
        +   timestamps: array of multiple multivariate time series timestamps corresponding to data
        +   files: array of file names that store the MTS
        +   aggregated_cols: aggregation daily data: sum of step counts, sum of calories, avg of Heartrate, max Heartrate, min Heartrate
        +   [4, 6, 7, 8, 9]: is the ids of the columns/features in the csv that you want to use in the MTS
        Please replace these with your data that you are using.
        """
        data, timestamps, files = preprocess.parse_band_data('./Dataset/Your-dataset/', [4, 6, 7, 8, 9], DISCARD_ZEROS)
        aggregated_cols = ['sum', 'sum', 'avg', 'max', 'min']
        for i in range(0, len(data)):
            # parse data
            p_data, p_aggregated_values, p_normed_aggregated_values, p_daily_timestamps = preprocess.parse_daily_band_data(
                data[i], timestamps[i], files[i], aggregated_cols)

            # compute corresponding labels
            """
            Please manually create folder aggregate, similarity, label, distance, date_order, graph to save the file.
            Otherwise, comment these LOCs
            """
            # visit_label, chemo_label = preprocess.create_label_for_band(data[i], timestamps[i], files[i],
            #                                                             aggregated_cols)
            # visit_label_file, chemo_label_file, similarity_file, distance_file, aggregate_file, normed_aggregate_file, order_file, graph_visit_file, graph_chemo_file, graph_pca_chemo_file = map(
            #     (lambda x: PREPROCESS_ATOMHP + x + files[i]), (
            #         '/label/visit_', '/label/chemo_', '/similarity/similarity_', '/distance/distance_',
            #         '/aggregate/aggregate_', '/aggregate/normed_aggregate_', '/date_order/order_',
            #         '/graph/graph_visit_',
            #         '/graph/graph_chemo_', '/graph/graph_pca_chemo_'))

            # dump data, label and statistics
            """
            Saving the data, and similarity matrix, and labels into files
            Comment these to ignore saving intermediate data
            """
            # np.savetxt(visit_label_file, visit_label)
            # np.savetxt(chemo_label_file, chemo_label)
            # np.savetxt(similarity_file, eros.eros(p_data).reshape((len(p_data), 1, len(p_data))))
            # np.savetxt(aggregate_file, p_aggregated_values)
            # np.savetxt(normed_aggregate_file, p_normed_aggregated_values)
            # np.savetxt(order_file, range(1, len(visit_label) + 1))

            # visit_label, chemo_label = preprocess.mapping_labels(visit_label, label_map), preprocess.mapping_labels(
            #     chemo_label, label_map)

            # a list of annotations, each is associated with one data point
            # annotations = [str(i + 1) + "_" + str(int(p_aggregated_values[i][0])) for i in range(len(chemo_label))]
            # annotations = [str(int(p_aggregated_values[i][0])) for i in range(len(chemo_label))]

            # mtsne using DTW distance metric
            # dtw_square_distance_matrix = distance_metric.dtw_distance_matrix(p_data, distance_file + '_dtw', recompute=True)
            # Y_2 = mtsne.mtsne(dtw_square_distance_matrix, 2)
            # Y_3 = mtsne.mtsne(dtw_square_distance_matrix, 3)

            # mtsne using Euclidean distance metric
            # eu_square_distance_matrix = eu_distance_matrix(p_data, distance_file, squared=True)
            # tsne.tsne(eu_square_distance_matrix, chemo_label, graph_chemo_file, annotations, 2)
            # tsne_old.tsne_old(eu_square_distance_matrix, chemo_label, graph_chemo_file, None, 3)

            # tsne using EROS similarity
            similarity_matrix = np.loadtxt(similarity_file);
            Y_2 = mtsne.mtsne(similarity_matrix, 2)     #2 dimensional
            Y_3 = mtsne.mtsne(similarity_matrix, 3)     #3 dimensional

            # PCA
            # Y_2 = pca.do_pca(p_normed_aggregated_values, 2)
            # Y_3 = pca.do_pca(p_normed_aggregated_values, 3)
            #
            # graph_plot.dump_graph(Y_2, chemo_label,graph_chemo_file,annotations,2)
            graph_plot.dump_graph(Y_3, chemo_label,graph_chemo_file,None,3)     #mtsne in 3-D space
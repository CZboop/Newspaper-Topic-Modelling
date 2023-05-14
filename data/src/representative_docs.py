import json
from pathlib import Path

# adjusting topic cluster plots to also show representative docs
# creating new plots rather than just overwriting
class RepresentativeDocsRepresenter:
    # relative paths to current parent directory, will use the source and naming conventions currently used to get each file
    def __init__(self, path_to_plot = 'plots', path_to_repr_docs = 'plots/topic_doc_examples', sources = ['telegraph', 'guardian', 'express', 'mail', 'sun', 'metro', 'mirror']):
        self.path_to_plot = path_to_plot # path to topic cluster plot, should have files <source_name>_topics.json to match source list in this object
        self.path_to_repr_docs = path_to_repr_docs # path to representative docs file, should have files <source_name>.json
        self.sources = sources # just name of source to get existing files with source in file name

    def _read_data(self, source):
        # reading in _topics.json file with topic cluster plot, storing as property of object
        with open(f'./{self.path_to_plot}/{source}_topics.json', 'r') as file_:
            self.plot = json.load(file_)
        # reading in .json file from directory with representative docs file (created from topic modeller class), storing as property of object
        with open(f'./{self.path_to_repr_docs}/{source}.json', 'r') as file_:
            self.repr_docs = json.load(file_)

    # adding representative doc to plotly plot and saving as a new file with example
    def add_repr_docs(self, source):
        # add into the custom data definition, new field for examples
        self.new_plot = self.plot
        self.new_plot["data"][0].update({"hovertemplate":"<b>Topic %{customdata[0]}</b><br>Words: %{customdata[1]}<br>Size: %{customdata[2]}<br>Example: %{customdata[3]}"})

        # add for each topic in the right format
        # append to custom data, array within array, based on filtering by first element which has the topic number
        max_topic_num = max([int(x) for x in self.repr_docs.keys()])
        for i in range(max_topic_num + 1):
            # update each topic custom data array within the plot json
            # they are all in order in the plot already, but not in the representative examples json
            current_data = self.new_plot["data"][0].get("customdata")[i]
            doc_for_current_topic = self.repr_docs.get(str(i))[0]
            # adding newlines every 5 words so doesn't spill over the hover tooltip
            if len(doc_for_current_topic.split(" ")) >= 5:
                example_split = doc_for_current_topic.split(" ")
                doc_for_current_topic = "<br>".join([' '.join(example_split[i: i + 5]) for i in range(0, len(example_split), 5)])

            # adding only first example, don't want to overcrowd hover
            current_data.append(doc_for_current_topic)
            self.new_plot["data"][0].get("customdata")[i] = current_data
        # saving new plot
        self.save_new_plot(f'./plots/plots_with_examples/{source}.json')
        return self.new_plot

    # saving updated/new plot to a json file
    def save_new_plot(self, path_to_save):
        with open(path_to_save, 'w') as file_:
            json.dump(self.new_plot, file_)

    # method that can be used to run all functionality in one pass
    def run_for_all_sources(self):
        all_plots = []
        for source in self.sources:
            self._read_data(source)
            all_plots.append(self.add_repr_docs(source))
        self.all_plots = all_plots
        return all_plots
# adjusting topic cluster plots to also show representative docs
# creating new plots rather than just overwriting
# TODO: handle errors/ mismatches between the two sets of data? just throw error if not same num for example
import json
from pathlib import Path

class RepresentativeDocsRepresenter:
    def __init__(self, path_to_plot, path_to_repr_docs, source):
        self.path_to_plot = path_to_plot
        self.path_to_repr_docs = path_to_repr_docs
        self.source = source
        self.current_path = Path(__file__).parent
        self._read_data()

    def _read_data(self):
        with open(f'{self.path_to_plot}', 'r') as file_:
            self.plot = json.load(file_)
        with open(f'{self.path_to_repr_docs}', 'r') as file_:
            self.repr_docs = json.load(file_)

    def add_repr_docs(self):
        # steps - 
        # add into the custom data - examples
        # append to below something similar
        # "hovertemplate":"<b>Topic %{customdata[0]}</b><br>Words: %{customdata[1]}<br>Size: %{customdata[2]}"
        self.new_plot = self.plot
        self.new_plot["data"][0].update({"hovertemplate":"<b>Topic %{customdata[0]}</b><br>Words: %{customdata[1]}<br>Size: %{customdata[2]}<br>Example: %{customdata[3]}"})
        print(self.new_plot["data"][0].get("hovertemplate"))
        # add for each in the right format
        # append to array based on filtering by first element which has the topic number
        max_topic_num = max([int(x) for x in self.repr_docs.keys()])
        for i in range(max_topic_num):
            # update each topic custom data array within the plot json
            # they are all in order in the plot already, but not in the representative examples json
            current_data = self.new_plot["data"][0].get("customdata")[i]
            doc_for_current_topic = self.repr_docs.get(str(i))[0]
            # adding newlines so doesn't spill over the hover tooltip
            if len(doc_for_current_topic.split(" ")) >= 5:
                example_split = doc_for_current_topic.split(" ")
                doc_for_current_topic = "<br>".join([' '.join(example_split[i: i + 5]) for i in range(0, len(example_split), 5)])

            # initially adding one example, don't want to overcrowd hover
            # could come back to or have another way of viewing all examples
            current_data.append(doc_for_current_topic)
            self.new_plot["data"][0].get("customdata")[i] = current_data

        self.save_new_plot(f'{self.current_path}/plots/plots_with_examples/{self.source}.json')

    def save_new_plot(self, path_to_save):
        with open(path_to_save, 'w') as file_:
            json.dump(self.new_plot, file_)

    def run_for_all_sources(self):
        pass

if __name__ == "__main__":
    path = Path(__file__).parent
    repr_docs = RepresentativeDocsRepresenter(f'{path}/plots/telegraph_topics.json', f'{path}/plots/topic_doc_examples/telegraph.json', 'telegraph')
    repr_docs.add_repr_docs()
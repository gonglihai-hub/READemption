import sys
from collections import defaultdict
from collections import Counter
from functools import reduce
from reademptionlib.fasta import FastaParser
import pysam
import pprint

class ReadAlignerStats(object):
    def __init__(self, references_by_speies):
        self.references_by_species = references_by_speies
        self.fasta_parser = FastaParser()

        """
        import itertools
        species = ["human", "virus", "bacteria"]
        cross_combos = []
        for combo_length in range(2, len(species) + 1):
            combos_of_length = list(itertools.combinations(species, combo_length))
            for combo_of_length in combos_of_length:
                cross_combos.append(combo_of_length)
        print(cross_combos)
        
        """

    def count(self, read_alignment_result_bam_path, unaligned_reads_path):
        self._stats = {}
        # Set up total stats
        self._stats["stats_total"] = defaultdict(float)
        self._init_stats_total()
        # Set up species stats
        self._stats["species_stats"] = defaultdict()
        for sp in self.references_by_species.keys():
            self._stats["species_stats"][sp] = defaultdict(float)
            self._init_species_dict(sp)
        self._count_aligned_reads_and_alignments(read_alignment_result_bam_path)
        self._count_unaligned_reads(unaligned_reads_path)
        return self._stats

    def _count_unaligned_reads(self, unaligned_read_paths):

        with open(unaligned_read_paths) as fasta_fh:
            self._stats["stats_total"][
                "no_of_unaligned_reads"
            ] = self._count_fasta_entries(fasta_fh)

    def _count_fasta_entries(self, fasta_fh):
        return reduce(
            lambda x, y: x + 1, self.fasta_parser.entries(fasta_fh), 0
        )

    def _count_aligned_reads_and_alignments(
        self, read_alignment_result_bam_path
    ):
        bam = pysam.Samfile(read_alignment_result_bam_path)

        bamfile = pysam.AlignmentFile(read_alignment_result_bam_path, 'rb')
        indexed_bam = pysam.IndexedReads(bamfile)
        # build index in memory
        indexed_bam.build()

        stats_per_ref = defaultdict(dict)
        no_of_hits_per_read_freq = {}
        for ref_id in bam.references:
            # Set up reference stats
            self._init_counting_dict(stats_per_ref, ref_id)
        for entry in bam.fetch():
            ref_id = bam.getrname(entry.tid)
            # Don't count the alignment if it is supplementary, to avoid
            # counting the same alignment multiple times
            if entry.is_supplementary:
                continue
            else:
                try:
                    self._count_alignment(
                        entry, ref_id, stats_per_ref, no_of_hits_per_read_freq,
                        indexed_bam
                    )
                except KeyError:
                    sys.stderr.write(
                        "SAM entry with unspecified reference found! Stoping\n"
                    )
                    sys.exit(2)
        self._stats["stats_per_reference"] = stats_per_ref
        for ref_id, stats in stats_per_ref.items():
            stats_per_ref[ref_id][
                "no_of_hits_per_read_and_freqs"
            ] = self._calc_down_to_read(
                stats_per_ref[ref_id]["no_of_hits_per_read_and_freqs"]
            )
        #self._stats["stats_total"] = self._sum_countings(stats_per_ref)

    def _bam_to_sam(self, bam_path, sam_path):
        pysam.view("-ho{}".format(sam_path), bam_path, catch_stdout=False)

    def _sum_countings(self, stats_per_ref):
        total_stats = {}
        for ref_id, stats in stats_per_ref.items():
            for attribute, value in stats.items():
                if type(value) is int or type(value) is float:
                    total_stats.setdefault(attribute, 0)
                    total_stats[attribute] += value
                elif type(value) is dict:
                    total_stats.setdefault(attribute, {})
                    for value_int, freq in value.items():
                        total_stats[attribute].setdefault(value_int, 0)
                        total_stats[attribute][value_int] += freq
        return total_stats

    def _calc_down_to_read(self, no_of_hits_per_read_freq):
        """As the frequencies were determined via the alignments we need
        to normalized each frequency value down to the read by
        dividing the frequencig by the number of hits per read.
        """
        return dict(
            (no_of_hits_per_read, freq / no_of_hits_per_read)
            for no_of_hits_per_read, freq in no_of_hits_per_read_freq.items()
        )
    def _init_stats_total(self):
        self._stats["stats_total"]["no_of_alignments"]
        self._stats["stats_total"]["no_of_aligned_reads"]
        #self._stats["stats_total"]["fractions_of_aligned_reads"] # deprecated
        self._stats["stats_total"]["no_of_split_alignments"]
        self._stats["stats_total"]["no_of_split_aligned_reads"]
        self._stats["stats_total"]["no_of_uniquely_aligned_reads"]
        self._stats["stats_total"]["no_of_multiple_aligned_reads"]
        self._stats["stats_total"]["alignment_length_and_freqs"] = defaultdict(int)
        self._stats["stats_total"]["no_of_hits_per_read_and_freqs"] = defaultdict(
            int
        )

    def _init_species_dict(self, species):
        sp = species
        self._stats["species_stats"][sp]["no_of_alignments"]
        self._stats["species_stats"][sp]["no_of_aligned_reads"]
        # self._stats["species_stats"][sp]["fractions_of_aligned_reads"] # deprecated
        self._stats["species_stats"][sp]["no_of_split_alignments"]
        self._stats["species_stats"][sp]["no_of_split_aligned_reads"]
        self._stats["species_stats"][sp]["no_of_uniquely_aligned_reads"]
        self._stats["species_stats"][sp]["no_of_multiple_aligned_reads"]
        self._stats["species_stats"][sp]["alignment_length_and_freqs"]  = defaultdict(int)
        self._stats["species_stats"][sp]["no_of_hits_per_read_and_freqs"] = defaultdict(
            int
        )

    def _init_counting_dict(self, stats_per_ref, ref_id):
        stats_per_ref[ref_id] = defaultdict(float)
        stats_per_ref[ref_id]["no_of_alignments"]
        stats_per_ref[ref_id]["no_of_aligned_reads"]
        # stats_per_ref[ref_id]["fractions_of_aligned_reads"] # deprecated
        stats_per_ref[ref_id]["no_of_split_alignments"]
        stats_per_ref[ref_id]["no_of_split_aligned_reads"]
        stats_per_ref[ref_id]["no_of_uniquely_aligned_reads"]
        stats_per_ref[ref_id]["no_of_multiple_aligned_reads"]
        stats_per_ref[ref_id]["alignment_length_and_freqs"] = defaultdict(int)
        stats_per_ref[ref_id]["no_of_hits_per_read_and_freqs"] = defaultdict(
            int
        )

    def _count_alignment(
        self, entry, ref_id, stats_per_ref, no_of_hits_per_read_freq, indexed_bam
    ):
        entry_tags_dict = dict(entry.tags)
        no_of_hits = entry_tags_dict["NH"]
        # check if alignment is unique or multiple
        if no_of_hits == 1:
            unique_alignment = True
        else:
            unique_alignment = False
        # check if alignment is split
        if "XH" in entry_tags_dict:
            split_alignment = True
        else:
            split_alignment = False
        # Add the alignment length frequencies to the chromosome
        stats_per_ref[ref_id]["alignment_length_and_freqs"][entry.reference_length] += 1
        # Add to total stats if the alignment is primary (=not secondary)
        if not entry.is_secondary:
            # is primary alignment
            # get the species by ref_id
            for sp, ref_ids in self.references_by_species.items():
                if ref_id in ref_ids:
                     ref_sp = sp

            # Count number of hits and frequencies for the library
            self._stats["stats_total"]["no_of_hits_per_read_and_freqs"][no_of_hits] +=1


            # TODO maybe changing the order to the case that happens the most
            # makes the program faster
            # Count split aligned read
            if (unique_alignment and split_alignment):
                # Add to chromosome
                # Add to number of split aligned reads of chromosome
                stats_per_ref[ref_id]["no_of_split_aligned_reads"] += 1
                # Add to number of aligned reads of chromosome
                stats_per_ref[ref_id]["no_of_aligned_reads"] += 1
                # Add to number of alignments of chromosome
                stats_per_ref[ref_id]["no_of_alignments"] += 1
                # Add to library
                # Add to number of split aligned reads of library
                self._stats["stats_total"]["no_of_split_aligned_reads"] += 1
                # Add to number of aligned reads of library
                self._stats["stats_total"]["no_of_aligned_reads"] += 1
                # Add to number of alignments of library
                self._stats["stats_total"]["no_of_alignments"] += 1
                # Add to species stats
                # Add to number of split aligned reads of species
                self._stats["species_stats"][ref_sp]["no_of_split_aligned_reads"] += 1
                # Add to number of aligned reads of species
                self._stats["species_stats"][ref_sp]["no_of_aligned_reads"] += 1
                # Add to number of alignments of species
                self._stats["species_stats"][ref_sp]["no_of_alignments"] += 1


            # Count uniquely aligned read
            elif (unique_alignment and not split_alignment):
                # Add to chromosome
                # Add to number of uniquely aligned reads of chromosome
                stats_per_ref[ref_id]["no_of_uniquely_aligned_reads"] += 1
                # Add to number of aligned reads of chromosome
                stats_per_ref[ref_id]["no_of_aligned_reads"] += 1
                # Add to number of alignments of chromosome
                stats_per_ref[ref_id]["no_of_alignments"] += 1
                # Add to library
                # Add to number of uniquely aligned reads of library
                self._stats["stats_total"]["no_of_uniquely_aligned_reads"] += 1
                # Add to number of aligned reads of library
                self._stats["stats_total"]["no_of_aligned_reads"] += 1
                # Add to number of alignments of library
                self._stats["stats_total"]["no_of_alignments"] += 1
                # Add to species stats
                # Add to number of uniquely aligned reads of species
                self._stats["species_stats"][ref_sp]["no_of_uniquely_aligned_reads"] += 1
                # Add to number of aligned reads of species
                self._stats["species_stats"][ref_sp]["no_of_aligned_reads"] += 1
                # Add to number of alignments of species
                self._stats["species_stats"][ref_sp]["no_of_alignments"] += 1

            # Count multiple aligned read
            elif (not unique_alignment and not split_alignment):
                # Add to number of aligned reads of library
                self._stats["stats_total"]["no_of_aligned_reads"] += 1
                # retrieve all alignments of the query
                alignments = indexed_bam.find(entry.query_name)
                # collect all reference names of alignments of query
                alignments_ref_seqs = []
                for alignment in alignments:
                    # do not collect supplementary alignments
                    if alignment.is_supplementary:
                        continue
                    alignments_ref_seqs.append(alignment.reference_name)
                for ref in alignments_ref_seqs:
                    # Add to number of alignments of chromosome
                    stats_per_ref[ref]["no_of_alignments"] += 1
                    # Add to number of alignments of library
                    self._stats["stats_total"]["no_of_alignments"] += 1


                # check if cross species aligned
                aligned_species = self._get_aligned_species(alignments_ref_seqs, self.references_by_species)
                if len(set(aligned_species)) > 1:
                    # cross aligned
                    for ref_sp in (set(aligned_species)):
                        # Add to number of aligned reads to species
                        self._stats["species_stats"][ref_sp]["no_of_aligned_reads"] += 1
                        # Add to number of cross aligned reads to species
                        self._stats["species_stats"][ref_sp]["no_of_cross_aligned_reads"] += 1
                    for ref_sp in aligned_species:
                        # Add to number of alignments to species
                        self._stats["species_stats"][ref_sp]["no_of_alignments"] += 1
                    # Add to number of cross aligned reads of library
                    self._stats["stats_total"]["no_of_cross_aligned_reads"] += 1
                    for ref in set(alignments_ref_seqs):
                        # Add to number of cross aligned reads of chromosome.
                        # A set is used to ensure that a read that maps multiple
                        # times to the same chromosome is counted only once for
                        # each chromosome.
                        # Add to number of cross aligned reads of chromosome
                        stats_per_ref[ref]["no_of_cross_aligned_reads"] += 1
                        # Add to number of aligned reads of chromosome
                        stats_per_ref[ref]["no_of_aligned_reads"] += 1


                else:
                    # multiple aligned
                    ref_sp = aligned_species[0]
                    # Add to number of aligned reads of species
                    self._stats["species_stats"][ref_sp]["no_of_aligned_reads"] += 1
                    # Add to number of multiple aligned reads of species
                    self._stats["species_stats"][ref_sp]["no_of_multiple_aligned_reads"] += 1
                    # Add to number of multiple aligned reads of library
                    self._stats["stats_total"]["no_of_multiple_aligned_reads"] += 1


                    for ref in set(alignments_ref_seqs):
                        # Add to number of multiple aligned reads of chromosome.
                        # A set is used to ensure that a read that maps multiple
                        # times to the same chromosome is counted only once for
                        # each chromosome
                        stats_per_ref[ref]["no_of_multiple_aligned_reads"] += 1
                        # Add to number of aligned reads of chromosome
                        stats_per_ref[ref]["no_of_aligned_reads"] += 1
                    for ref_sp in aligned_species:
                        # Add to number of alignments to species
                        self._stats["species_stats"][ref_sp]["no_of_alignments"] += 1



    def _get_aligned_species(self, alignment_ref_seqs, references_by_species):
        aligned_species = []
        for species, references in references_by_species.items():
            for ref_seq in alignment_ref_seqs:
                if ref_seq in references:
                    aligned_species.append(species)
        return aligned_species

        # if primary: add to total stats
        # check if uniquely aligned
        # check if split aligned:
        # check if cross-mapped
        # check if multiple aligned
        # check if cross-mapped
        # or add to species
        # add to chromosome
        # check if uniquely aligned
        # check if split aligned
        # check if multiple aligned
        # check if cross-mapped
        # or add to species




       #overview of algorithm option A
         # check if primary alignment (not secondary)
         # if primary: add to total stats
            # add to number of hits and read freqs
            # check if uniquely aligned
            # check if split aligned:
                # check if cross-mapped
            # check if multiple aligned
                # check if cross-mapped
                # or add to species
        # add to chromosome
            # check if uniquely aligned
            # check if split aligned
            # check if multiple aligned
                # check if cross-mapped
                # or add to species

"""
        no_of_hits = entry_tags_dict["NH"]
        number_of_split_alignments_within_this_SAM_record = float(
            entry_tags_dict.get("XH", 1)
        )
        total_number_of_split_alignments_for_the_whole_read = float(
            entry_tags_dict.get("XJ", 1)
        )
        proportion_of_total_split_alignments_of_the_whole_read_for_this_sam_record = (
            number_of_split_alignments_within_this_SAM_record
            / total_number_of_split_alignments_for_the_whole_read
        )
        # If the SAM-tag XH exists, the alignment is a split alignment
        if "XH" in entry_tags_dict:
            # add to the number of split reads for the chromosome
            # Is it possible that a split maps collinear and split?
            # No, because read splitting is only triggered when a read can not
            # be mapped collinear
            # Only add the read if it is the primary alignment. Otherwise the read will be counted multiple times
            # Although this behaviour doesn't exist for segemehl, it could exist in other aligners.

            # count the number of split alignments for the chromosome
            stats_per_ref[ref_id][
                "no_of_split_alignments"
            ] += proportion_of_total_split_alignments_of_the_whole_read_for_this_sam_record
            stats_per_ref[ref_id]["no_of_hits_per_read_and_freqs"][
                no_of_hits
            ] += (
                1.0
                / (
                    float(no_of_hits)
                    * proportion_of_total_split_alignments_of_the_whole_read_for_this_sam_record
                )
            )
            stats_per_ref[ref_id][
                "no_of_alignments"
            ] += proportion_of_total_split_alignments_of_the_whole_read_for_this_sam_record
            stats_per_ref[ref_id]["no_of_aligned_reads"] += (
                proportion_of_total_split_alignments_of_the_whole_read_for_this_sam_record
                / (float(no_of_hits))
            )
        else:
            stats_per_ref[ref_id]["no_of_alignments"] += 1.0
            stats_per_ref[ref_id]["no_of_aligned_reads"] += 1.0 / (
                float(no_of_hits)
            )
        stats_per_ref[ref_id]["no_of_hits_per_read_and_freqs"][
            no_of_hits
        ] += proportion_of_total_split_alignments_of_the_whole_read_for_this_sam_record
        if no_of_hits == 1:
            stats_per_ref[ref_id]["no_of_uniquely_aligned_reads"] += (
                1.0
                / proportion_of_total_split_alignments_of_the_whole_read_for_this_sam_record
            )
        stats_per_ref[ref_id]["alignment_length_and_freqs"][entry.alen] += 1
"""

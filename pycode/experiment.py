"""PyCode experiment classes.

Author: Mascelli Leonardo
Last edited: 23-10-2023

Here are contained the main structures that are used to contain the data
recorded during the experiments.
"""

from typing import Any, Dict, List, Optional, Tuple

from pathlib import Path
import numpy as np


class Signal:
    """
    Signal is a class that hold datas from a raw recording as it is. Useful in
    same cases are other informations that this class take record of, like:
    - sampling_frequency
    - path of the data in the filesystem
    - some user's notes
    """

    def __init__(self, data: np.ndarray, sampling_frequency: float, note: str =
                 "", path: Optional[Path] = None):
        self.data = data
        self.sampling_frequency = sampling_frequency
        self.note = note
        self.path = path


class PhaseInfo:  # just for the linter complains
    pass


class PhaseInfo:
    """
    Collection of information about an experiment phase. Useful for conversion.
    """

    def __init__(self):
        self.digital_notes = None

    def default_parse(self, filename: Path) -> PhaseInfo:
        """
        This method if where the naming convenction of the mcd ror h5 files is
        used for generate the metadata of the phase.

        the name must be in the form:

        [COLTURE-ID]_DIV[DAY-IN-VITRO]_[PHASE-TYPE]_[PHASE-ORDER]_[OTHER].extension

        !!! IF YOU WANT THE METADATA AUTOMATICALLY COMPUTED YOU MUST RESPECT
        THIS CONVENCTION, OTHERWISE YOU MUST SUPPLY THE METADATA MANUALLY OR
        CHANGE/OVERRIDE THIS FUNCTION TO ADAPT TO YOUR CONVENCTION !!!
        """
        try:
            arg_list = filename.name[:filename.name.rfind('.')].split(sep="_")
            self.name = arg_list[0]
            self.div = int(arg_list[1][arg_list[1].find("DIV") + 3:])
            phase_type_label = arg_list[2]
            self.digital = phase_type_label.upper() == "STIM"
            self.order = int(arg_list[3])
            self.other = None
            if len(arg_list) > 4:
                self.other = arg_list[4]
        except Exception as e:
            print(f"ERROR: PhaseInfo.default_parse. {e.args}")
        return self

    def add_digital_notes(self, notes: str):
        self.digital_notes = notes


class Phase:
    """
    The Phase class hold the informations about a single registration, that
    conceptually, is characterized by a different meaning respect to the
    others. For example it could be a recording taken during a stimulation of
    basal activity, and still it could be a basal activity taken before or
    after a stimulation or a stimulation with different parameters than an
    other.
    All this informations are stored in this class:
    - name: is the name of the mcd file containing the original recordings
    - peaks: is a map [electrode number -> time of the revealed peaks]
    - digital: if the phase was a stimulation is the Signal representing the
               presence of stimulation or less.
    - sampling frequency: self explainatory
    - durate: the duration in seconds of the recording
    - notes: some user notes about the recording
    """

    def __init__(
        self,
        name: str,
        peaks: Dict[int, np.ndarray],
        digital: Optional[Signal],
        sampling_frequency: float,
        durate: float,
        notes: str,
    ):
        self.name = name
        self.peaks = peaks
        self.digital = digital
        self.sampling_frequency = sampling_frequency
        self.durate = durate
        self.div: Optional[int] = None
        self.phase_type: Optional[str] = None
        self.order: Optional[int] = None
        self.rest: str = ""
        self.notes = notes
        self.parse_phase()

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__()

    def parse_metadata(self):
        """
        This method if where the naming convenction of the mcd files is used
        for generate the metadata of the phase.

        the name must be in the form:

        [COLTURE-ID]_DIV[DAY-IN-VITRO]_[PHASE-TYPE]_[PHASE-ORDER]_[OTHER].mcd

        !!! IF YOU WANT THE METADATA AUTOMATICALLY COMPUTED YOU MUST RESPECT
        THIS CONVENCTION, OTHERWISE YOU MUST SUPPLY THE METADATA MANUALLY OR
        CHANGE THIS FUNCTION TO ADAPT TO YOUR CONVENCTION !!!
        """
        try:
            arg_list = self.name.split(sep="_")
            self.div = int(arg_list[1][arg_list[1].find("DIV") + 3:])
            self.phase_type = arg_list[2]
            self.order = int(arg_list[3])
            self.other = None
            if len(arg_list) > 4:
                self.other = arg_list[4]
        except Exception as e:
            print(f"Error parsing phase: {self.name} : {e.args}")

    def __dict__(self):
        ret = {
            "name": self.name,
            "digital": self.digital.data
            if self.digital is not None
            else np.zeros(shape=(1)),
            "peaks": None,
            "type": self.phase_type,
            "order": self.order,
            "sampling_frequency": self.sampling_frequency,
            "durate": self.durate,
            "notes": self.notes,
        }
        peaks = []
        for p in self.peaks:
            peaks.append((p, self.peaks[p]))
        ret["peaks"] = np.array(peaks, dtype=object)  # type: ignore

        return ret

    def info(self) -> str:
        type = self.phase_type if self.phase_type is not None else 'Unknown'
        div = self.div if self.div is not None else 'Unknown'
        order = self.order if self.order is not None else 'Unknown'
        durate = self.durate if self.durate is not None else 'Unknown'
        sampling_frequency = self.sampling_frequency\
            if self.sampling_frequency is not None else 'Unknown'
        return (
            f"type: {type}, "
            f"div: {div}, "
            f"order: {order}, "
            f"durate: {durate} seconds, "
            f"sampling frequency: {sampling_frequency} Hz"
        )

    def __str__(self):
        return self.name


class Experiment:
    """This class is meant to store information about all recording on a
    cellular colture and the information related to them. In particular, it has
    the following fields:
    - name: usually the colture id
    - path: path where the SpyCode files from whom it has been originated were
    - phases: a list of the experiment phases
    - date: date of the reconrdings
    - grounded_el: a list of channels grounded during recording
    - applied_operations: a list of tuple (operation_name, operation_arguments)
      applied to the experiment. The idea behind this field is that the user
      should apply operations using the experiment method *apply_operation*
      that automatically adds it on this list.
    """

    def __init__(self, name, path: str, date: str, phases: List[Phase],
                 grounded_el=[]):
        self.name = name
        self.path = path
        self.phases = phases
        self.date = date
        self.grounded_el: List[int] = grounded_el
        self.applied_operations: List[Tuple[str, List[str]]] = []

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__()

    def __dict__(self):
        ret = {
            "matrix_name": self.name,
            "path": self.path,
            "date": self.date,
            "phases": None,
        }
        phases = []
        for p in self.phases:
            phases.append(p.to_dict())
        ret["phases"] = np.array(phases, dtype=object)  # type: ignore
        return ret

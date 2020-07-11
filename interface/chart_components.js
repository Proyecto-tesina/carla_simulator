class RowComponent {
    constructor(data) {
        this.data = data;
        this.data.forEach((data) => data[0] = new Date(data[0]));
    }

    remove_description(data) {
        return data.map(e => e[0])
    }
}

class CameraDetectionComponent extends RowComponent {

    detections() {
        let detections = this.data.filter((data) => data[1] == 'I see you');
        return this.remove_description(detections);
    }

    non_detections() {
        let non_detections = this.data.filter((data) => data[1] == 'I don\'t see you');
        return this.remove_description(non_detections);
    }

    next_detection(non_detection) {
        let next_detections = this.detections().filter(
            (detection) => detection >= non_detection
        )

        return next_detections.length ? next_detections[0] : non_detection
    }

    distraction_row() {
        return this.non_detections().map(
            (non_detection, i) => [
                'Distraction time',
                'Camera NO detection' + ' ' + i,
                non_detection,
                this.next_detection(non_detection)
            ]
        );
    }

    rows() {
        return [this.distraction_row()];
    }
}

class DrtMonitorComponent extends RowComponent {

    drt_on_intervals() {
        let drts_on = this.data.filter((data) => data[1] != "mistake");
        return this.remove_description(drts_on);
    }

    mistakes() {
        let mistakes = this.data.filter((data) => data[1] == "mistake");
        return this.remove_description(mistakes);
    }

    drt_on_row() {
        let drts_on = this.drt_on_intervals()

        var rows = [];
        for (var i = 0; i < drts_on.length; i += 2) {
            let description = 'DRT on';
            let name = 'Light' + ' ' + i / 2;
            let start = drts_on[i];
            let end = drts_on[i + 1];

            rows.push([description, name, start, end]);
        }

        return rows;
    }

    mistakes_row() {
        return this.mistakes().map(
            (mistake, i) => ['Mistakes', 'Mistake' + ' ' + i, mistake, mistake]
        );
    }

    rows() {
        return [this.drt_on_row(), this.mistakes_row()]
    }
}

class PlayerActionComponent extends RowComponent {

    player_actions_row() {
        return this.data.map(
            (data) => [
                data[1],
                data[1],
                data[0],
                data[0]
            ]
        );
    }

    rows() {
        return [this.player_actions_row()]
    }
}
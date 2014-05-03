// taken from http://stackoverflow.com/questions/5915096/get-random-item-from-javascript-array

Array.prototype.sample = function () {
  return this[Math.random() * this.length | 0];
};

Array.prototype.shuffle = function () {
  for (var i = this.length; i > 0; --i)
    this.push(this.splice(Math.random() * i | 0, 1)[0]);
  return this;
};

(function(window, $, undefined) {
    var name_part_1 = ["Hack", "Soft", "Prag", "Code", "Target", "Software"]
    var name_part_2 = ["Bulgaria", "Academy", "Acad", "Code", "Training", "University", "School"]
    var types = ["Софтуерна Академия", "Обучителен център", "Обучителна Академия", "Училище за Програмисти", "IT обучителен център", "Софтуерно Училище", "Академия по Програмиране"]

    var team_qualities_part_1 = ["млади професионалисти", "професионлисти с опит в бранша", "прагматици", "разбиращи от бизнес процесите на IT индустрията хора"]
    var team_qualities_part_2 = ["най-новите технологии в момента", "иновативните практики на IT средата", "съвременни начини на мислене в обучението на IT кадри"]

    var course_buzzwords = ["практически-насочени", "с голям обхват", "използват съвременни средства за програмиране", "свързани с модерни софтуерни технологии", "отговарят на нуждата на IT средата", "ключови за успешното усвояване на бързо развиващите се технологии"]

    var believe_buzzwords = ["успещно подобряваме IT индустрията", "спомагаме за успешното развитие на IT бранша", "курсовете ни отговарят на изискванията на IT средата за растеж"]

    var teacher_buzzwords = ["богат опит в бранша", "собствени приложения с истински клиенти", "съвременен поглед върху обучителния процес", "дългосрочна практика", "визионерско виждане за IT индустрията", "следят най-горещите тенденции в сферата на софтуера"]

    var mission_buzzwords = ["нужните практически умения", "знанията, които ще ги направят добри софтуерни инженери", "най-доброто практическо обучение за нуждите на бранша", "сечението между академичното и практичното"]

    function format(str, d) {
        for(key in d) {
            str = str.replace("{" + key + "}", d[key]);
        }

        return str;
    };

    function plural_phrase(arr) {
        var last_one = arr.pop();
        return arr.join(", ") + " и " + last_one
    }

    function sample_name() {
        return name_part_1.sample() + name_part_2.sample()
    };

    function sample_type() {
        return types.sample()
    };

    function sample_team(how_many) {
        var qualities = [];
        team_qualities_part_1.shuffle();
        qualities = team_qualities_part_1.slice(0, how_many);

        return plural_phrase(qualities);
    };

    function sample_course_buzzwords() {
        course_buzzwords.shuffle()
        var buzzwords = course_buzzwords.slice(0, 3)

        return plural_phrase(buzzwords);
    };

    function sample_believe_buzzwords() {
        return believe_buzzwords.sample();
    };

    function sample_qualities() {
        return team_qualities_part_2.sample();
    };

    function sample_teacher_buzzwords(how_many) {
        teacher_buzzwords.shuffle()
        result = teacher_buzzwords.slice(0, how_many)

        return plural_phrase(result);
    };

    function sample_mission_buzzwords(how_many) {
        mission_buzzwords.shuffle();
        result = mission_buzzwords.slice(0, how_many);
        return plural_phrase(result);
    };

    window.DescriptionGenerator = {
        give_me_new_one : function() {
            console.log(format)
            var
                name = sample_name(),
                final_text = [];

            final_text.push(format("{name} е {type} за курсове по програмиране", {
                    name : name,
                    type : sample_type()
            }));

            final_text.push(format("{name} е съставен от екип от {team}, които имат достъп до {qualities}.", {
                    name : name,
                    team : sample_team(3),
                    qualities : sample_qualities()
            }));

            final_text.push(format("Нашите обучения са {course_buzzwords}, като вярваме, че {believe_buzzwords}!", {
                    course_buzzwords : sample_course_buzzwords(),
                    believe_buzzwords : sample_believe_buzzwords()
            }));

            final_text.push(format("Нашите преподаватели имат {teacher_buzzwords}!", {
                    teacher_buzzwords : sample_teacher_buzzwords(2)
            }));

            final_text.push(format("Нашата мисия е да дадем на хората {mission_buzzwords}!", {
                    mission_buzzwords : sample_mission_buzzwords(2)
            }));

            return final_text.join("\n")
        }
    };

})(window, jQuery)

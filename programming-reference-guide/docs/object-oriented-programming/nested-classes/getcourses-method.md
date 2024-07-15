<h1> GetCourses Method</h1>

```apl

    ∇ R←GetCourses;COURSECODES;COURSES;INDEX
      :Access Public
      COURSECODES COURSES INDEX←⎕FREAD GOLFID 1
      R←{⎕NEW GolfCourse ⍵}¨↓⍉↑COURSECODES COURSES
    ∇
```

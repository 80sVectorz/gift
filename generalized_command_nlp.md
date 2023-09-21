# Brainstorm for generalized command interpretation and verb implementation

## Examples of different inputs
```
Take the apple.

Consume the juicy apple.

Consume the apple and the pear.

Consume the apple, the banana and the pear

Open the door.

Enter the door.

Chop the tree down using the axe.

Use the axe to chop the tree down.
```

### Break down

```
Take the apple -> **[verb] [junk] [object reference]**

Consume the red apple -> **[verb] [junk] [filter] [object reference]**

Consume the apple and the pear -> **[verb] [junk] [object reference] [addition] [junk] [object reference]**

Consume the apple, the banana and the pear -> **[verb] [junk] [object reference] [addition] [junk] [object reference] [addition] [junk] [object reference]**

Open the door -> **[verb] [junk] [object reference]**

Enter the door -> **[verb] [junk] [object reference]**

Chop the tree down using the axe -> **[verb] [junk] [object reference] [verb specific junk] [verb modifier] [junk] [object reference]**

Use the axe to chop the tree down -> **[reversed verb modifier] [junk] [object reference] [reversed verb modifier split] [verb] [junk] [object reference] [verb specific junk]**

Place the candle on the table -> **[verb] [junk] [object reference] [verb specific split] [junk] [object/surface reference]**
```
### Filtered by removing junk
If we remove all junk words the sentence should still work. Removing the junk is done by checking if a word is in the junk list which mostly includes 'the' in this case. Or if the word is in the verbs junk list. Verbs should be easy to find by checking if a word is in the verb list.
Preferably we should be able to type already filtered sentences and interpret them as normal. So typing "Take apple." should work just as well as "Take the apple".
```
Take apple -> **[verb] [object reference]**

Consume red apple -> **[verb] [filter] [object reference]**

Consume apple and pear -> **[verb] [object reference] [addition] [object reference]**

Consume apple, banana and pear -> **[verb] [object reference] [addition] [object reference] [addition] [object reference]**

Open door -> **[verb] [object reference]**

Enter door -> **[verb] [object reference]**

Chop tree using axe -> **[verb] [object reference] [verb modifier] [object reference]**

Use axe to chop tree -> **[reversed verb modifier] [object reference] [reversed verb modifier split] [verb] [object reference]**

Place candle on table -> **[verb] [object reference] [verb specific split] [object/surface reference]**
```
### Observations

In all the examples the verbs we find they can be reduced into one form. Which is:

**[verb] [argument e.g object or surface]**

Some of these can be made more specific with a verb modifier.
for example we can imagine "Chop tree" would make the program automatically use the best tool so it would say:
"You chop the tree down using your axe" if you don't specificy you want to use your walking cane. 
Or for "Place candle" it would choose a nearby prefered storage surface e.g a table, unless you type "Place candle on the floor" for example.
We al also see 'filters' these let you filter for a certain trait. for example say you have a set of magical crystals each with a different color, to grab the green crystal you would type "Grab the green crystal" this rules out all the other colors. Now what happens when you don't filter for a specific crystal. Preferably the program should say something like this "There are multiple crystals please specify which one.". All these features need to be easy to implement so with as little hassle as possible.

#### Traits and properties
All of the features of automatically choosing imply that the program has to understand which object are suitable for which task.
We aren't working with neural networks here so we will have to write a generalized and elegant but manual approach.
Let's start with the crystal example.
Simple would be to give each crystal a tag/property for example "green" or "red".
But I think it is best to define traits as a custom data type. I'll give an example:
Say we make a color trait and it has a few different values like "red" and "green". We can give this trait to different objects. And it works the same for all of the objects. Most likely some traits will be on almost all objects color would be one of them probably. Now you can be sure that color works the same for all objects. This also makes modding and adding content more streamlined.

The same system could be used to give weapons a 'sharp' trait that can be useful when the program has to select the best tool to chop down a tree with.
The way the program chooses would be defined in the verb it self.

#### "Eat it"
Eat it? Eat what? A common word used in the english language is 'it' computers struggle with this word. 'it' can refer to any previous mentioned noun.
An interesting example is: "I spread a cloth on the table in order to protect it". 
Obviously 'it' refers to the table but you need to know what a cloth is.
Because you have experience with table cloths and/or reality you can infer that the 'it' refers to the table using your understanding of the world.
In our case the problem is not as difficult as we always do something and never state something.
So if we keep track of previously interacted objects.
We can quite confidently say that the last object is the referent.
This only applies though when only one object is used.
We can interpret a set of commands like "grab the axe" and then "chop the tree down with it" this way.
This system may not always do what the user wants so prompting if the 'it' is infered correctly is probably good practice e.g "chop the tree down with it. -> by 'it' do you mean the axe? yes/no: ".

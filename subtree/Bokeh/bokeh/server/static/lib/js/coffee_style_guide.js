// Generated by CoffeeScript 1.3.3
(function() {
  "start of continuum CS style guide. our code does not follow this yet.";

  "2 spaces per indent\n80 characters per line";

  "underscores to separate variables names\nCamelCase for class names\nunderscores preceding functions show what we think is private\ncoffeescript makes it easy to pass instance methods as callbacks.\ntry to use that instead of writing lots of inline functions as callbacks";

  var MyBigClass, foo,
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  MyBigClass = (function(_super) {

    __extends(MyBigClass, _super);

    function MyBigClass() {
      return MyBigClass.__super__.constructor.apply(this, arguments);
    }

    MyBigClass.prototype.set_my_field = function() {
      this.set('hello');
      return MyBigClass.__super__.set_my_field.call(this);
    };

    MyBigClass.prototype._dont_call_func = function() {
      return console.log('you should not be calling this');
    };

    MyBigClass.prototype.call_func = function() {
      console.log('but I can call this func, because I am in this class');
      return this._dont_call_func();
    };

    return MyBigClass;

  })(Backbone.Model);

  "coffee script looseness\nALWAYS use parentheses around function calls";


  console.log('log this statement');

  console.log('logging this message');

  foo = {
    coffee: 'black',
    cream: 'none',
    bagels: {
      cream_cheese: 'fat_free',
      toasted: 'of course'
    }
  };

  foo({
    'name': 'firstobject',
    'title': 'first'
  }, {
    'name': 'second object',
    'title': 'first'
  });

  foo({
    'name': 'second object',
    'title': 'first'
  }, {
    'name': 'second object',
    'title': 'first'
  });

  foo({
    'name': 'second object',
    'title': 'first'
  }, {
    'name': 'second object',
    'title': 'first'
  }, [1, 2, 3, 4, 5]);

  "inline functions\nwe follow the same syntax for object arrays.  4 spaces before the start of the\nfunction definition.  2 spaces before the comma separating the functions";


  foo(1, 2, 3, function() {
    var a;
    my_callback_goes_here();
    a = {
      'node': 'fast'
    };
    return a;
  }, function() {
    return second_callback_goes_here();
  });

  "return values\ncoffee script always returns the last value in a function.  don't rely on this.\nalways return something, or null";


}).call(this);
